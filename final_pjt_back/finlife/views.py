from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from datetime import datetime
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption
from .serializers import DepositProductSerializer, SavingProductSerializer


@api_view(['GET'])
def exchange(request):
    today = datetime.now().strftime('%Y%m%d')
    
    response = requests.get(
        'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON',
        params={
            'authkey': settings.KOREAEXIM_API_KEY,
            'searchdate': today,
            'data': 'AP01'
        },
        verify=False
    )
    
    if response.status_code != 200:
        return Response({'error': '환율 정보를 가져오는데 실패했습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = response.json()
    processed_data = [{
        'currency_code': item['cur_unit'],
        'rate': item['deal_bas_r'],
        'updated_at': today
    } for item in data]
    
    return Response(processed_data)


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