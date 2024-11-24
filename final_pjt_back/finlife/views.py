from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from datetime import datetime, timedelta
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption
from .serializers import DepositProductSerializer, SavingProductSerializer


@api_view(['GET'])
def exchange(request):
    def get_last_friday():
        today = datetime.now()
        # 오늘이 월요일(0)부터 일요일(6)까지일 때, 지난 금요일까지의 차이를 계산
        days_to_subtract = (today.weekday() - 4) % 7
        if days_to_subtract == 0 and today.hour < 11:  # 금요일이지만 11시 이전이면
            days_to_subtract = 7  # 지난주 금요일 데이터 사용
        last_friday = today - timedelta(days=days_to_subtract)
        return last_friday.strftime('%Y%m%d')

    def get_exchange_rate(date):
        response = requests.get(
            'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON',
            params={
                'authkey': settings.KOREAEXIM_API_KEY,
                'searchdate': date,
                'data': 'AP01'
            },
            verify=False,
            timeout=10
        )
        return response

    try:
        # 가장 최근 금요일 날짜로 시도
        friday_date = get_last_friday()
        response = get_exchange_rate(friday_date)
        
        if response.status_code == 200:
            data = response.json()
            if data:  # 데이터가 있는 경우
                processed_data = [{
                    'currency_code': item['cur_unit'],
                    'rate': item['deal_bas_r'],
                    'currency_name': item.get('cur_nm', ''),
                    'updated_at': friday_date
                } for item in data]
                return Response({
                    'status': 'success',
                    'message': '환율 정보를 성공적으로 가져왔습니다.',
                    'data': processed_data
                })
            else:  # 데이터가 비어있는 경우
                return Response({
                    'status': 'error',
                    'message': '환율 정보가 없습니다. 다음 영업일을 기다려주세요.'
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'status': 'error',
            'message': '환율 정보를 가져오는데 실패했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except requests.exceptions.RequestException as e:
        return Response({
            'status': 'error',
            'message': f'API 연결 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# 정기예금 상품 정보 (저장/갱신)
# 은행명, 상품명, 가입 방법, 금리 옵션 정보 
@api_view(['GET'])
def save_deposit_products(request):
    url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': settings.PROD_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return Response({'error': '데이터를 가져오는데 실패했습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = response.json()
    baseList = data.get('result').get('baseList')
    optionList = data.get('result').get('optionList')
    
    saved_products = []
    for item in baseList:
        product, created = DepositProduct.objects.get_or_create(
            fin_prdt_cd=item['fin_prdt_cd'],
            defaults={
                'kor_co_nm': item['kor_co_nm'],
                'fin_prdt_nm': item['fin_prdt_nm'],
                'etc_note': item.get('etc_note', ''),
                'join_way': item.get('join_way', ''),
                'join_deny': item.get('join_deny', ''),
                'join_member': item.get('join_member', ''),
            }
        )
        
        if not created:
            product.kor_co_nm = item['kor_co_nm']
            product.fin_prdt_nm = item['fin_prdt_nm']
            product.etc_note = item.get('etc_note', '')
            product.join_way = item.get('join_way', '')
            product.join_deny = item.get('join_deny', '')
            product.join_member = item.get('join_member', '')
            product.save()
            
            product.options.all().delete()
        
        options = [opt for opt in optionList if opt['fin_prdt_cd'] == product.fin_prdt_cd]
        saved_options = []
        for option in options:
            try:
                intr_rate = float(option.get('intr_rate', 0))
            except (TypeError, ValueError):
                intr_rate = 0.0
                
            try:
                save_trm = int(option.get('save_trm', 0))
            except (TypeError, ValueError):
                save_trm = 0
                
            saved_options.append({
                'fin_prdt_cd': option['fin_prdt_cd'],
                'intr_rate_type': option.get('intr_rate_type', ''),
                'intr_rate': intr_rate,
                'save_trm': save_trm
            })
        
        saved_products.append({
            'fin_prdt_cd': product.fin_prdt_cd,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'options': saved_options
        })
    
    return Response({
        'message': '정기예금 데이터 저장완료',
        'data': {
            'count': len(saved_products),
            'products': saved_products
        }
    })


# 정기적금 상품 정보 (저장/갱신)
# 기본 정보 및 금리 옵션 정보 
@api_view(['GET'])
def save_saving_products(request):
    url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    params = {
        'auth': settings.PROD_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return Response({'error': '데이터를 가져오는데 실패했습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = response.json()
    baseList = data.get('result').get('baseList')
    optionList = data.get('result').get('optionList')
    
    saved_products = []
    for item in baseList:
        product, created = SavingProduct.objects.get_or_create(
            fin_prdt_cd=item['fin_prdt_cd'],
            defaults={
                'kor_co_nm': item['kor_co_nm'],
                'fin_prdt_nm': item['fin_prdt_nm'],
                'etc_note': item.get('etc_note', ''),
                'join_way': item.get('join_way', ''),
                'join_deny': item.get('join_deny', ''),
                'join_member': item.get('join_member', ''),
            }
        )
        
        if not created:
            product.kor_co_nm = item['kor_co_nm']
            product.fin_prdt_nm = item['fin_prdt_nm']
            product.etc_note = item.get('etc_note', '')
            product.join_way = item.get('join_way', '')
            product.join_deny = item.get('join_deny', '')
            product.join_member = item.get('join_member', '')
            product.save()
            
            product.options.all().delete()
        
        options = [opt for opt in optionList if opt['fin_prdt_cd'] == product.fin_prdt_cd]
        saved_options = []
        for option in options:
            try:
                intr_rate = float(option.get('intr_rate', 0))
            except (TypeError, ValueError):
                intr_rate = 0.0
                
            try:
                save_trm = int(option.get('save_trm', 0))
            except (TypeError, ValueError):
                save_trm = 0
                
            saved_option = SavingOption.objects.create(
                product=product,
                fin_prdt_cd=option['fin_prdt_cd'],
                intr_rate_type=option.get('intr_rate_type', ''),
                intr_rate=intr_rate,
                save_trm=save_trm
            )
            
            saved_options.append({
                'fin_prdt_cd': saved_option.fin_prdt_cd,
                'intr_rate_type': saved_option.intr_rate_type,
                'intr_rate': saved_option.intr_rate,
                'save_trm': saved_option.save_trm
            })
        
        saved_products.append({
            'fin_prdt_cd': product.fin_prdt_cd,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'options': saved_options
        })
    
    return Response({
        'message': '정기적금 데이터 저장완료',
        'data': {
            'count': len(saved_products),
            'products': saved_products
        }
    })


# DB에 저장된 모든 정기예금 상품 정보 조회 (단순 조회)
@api_view(['GET'])
def get_deposit_products(request):
    products = DepositProduct.objects.all()
    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data)


# DB에 저장된 모든 정기적금 상품 정보 조회 (단순 조회)
@api_view(['GET'])
def get_saving_products(request):
    products = SavingProduct.objects.all()
    serializer = SavingProductSerializer(products, many=True)
    return Response(serializer.data)