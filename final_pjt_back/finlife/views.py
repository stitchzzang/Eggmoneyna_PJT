from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from datetime import datetime, timedelta
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption
from .serializers import DepositProductSerializer, SavingProductSerializer
import json
import os


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
                'max_limit': item.get('max_limit', None),
                'dcls_strt_day': item.get('dcls_strt_day', ''),
                'dcls_end_day': item.get('dcls_end_day', ''),
                'fin_co_subm_day': item.get('fin_co_subm_day', '')
            }
        )
        
        if not created:
            # 기존 상품 정보 업데이트
            for field in ['kor_co_nm', 'fin_prdt_nm', 'etc_note', 'join_way', 
                         'join_deny', 'join_member', 'max_limit', 'dcls_strt_day',
                         'dcls_end_day', 'fin_co_subm_day']:
                setattr(product, field, item.get(field, ''))
            product.save()
            
            # 기존 옵션 삭제
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
                
            saved_option = DepositOption.objects.create(
                product=product,
                fin_prdt_cd=option['fin_prdt_cd'],
                intr_rate_type=option.get('intr_rate_type', ''),
                intr_rate=intr_rate,
                save_trm=save_trm,
                intr_rate2=float(option.get('intr_rate2', 0)),
                rsrv_type=option.get('rsrv_type', '')
            )
            
            saved_options.append({
                'fin_prdt_cd': saved_option.fin_prdt_cd,
                'intr_rate_type': saved_option.intr_rate_type,
                'intr_rate': saved_option.intr_rate,
                'save_trm': saved_option.save_trm,
                'intr_rate2': saved_option.intr_rate2,
                'rsrv_type': saved_option.rsrv_type
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
                'max_limit': item.get('max_limit', None),
                'dcls_strt_day': item.get('dcls_strt_day', ''),
                'dcls_end_day': item.get('dcls_end_day', ''),
                'fin_co_subm_day': item.get('fin_co_subm_day', '')
            }
        )
        
        if not created:
            # 기존 상품 정보 업데이트
            for field in ['kor_co_nm', 'fin_prdt_nm', 'etc_note', 'join_way', 
                         'join_deny', 'join_member', 'max_limit', 'dcls_strt_day',
                         'dcls_end_day', 'fin_co_subm_day']:
                setattr(product, field, item.get(field, ''))
            product.save()
            
            # 기존 옵션 삭제
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
    try:
        products = DepositProduct.objects.all()
        
        # 각 상품의 상세 정보를 포함한 데이터 구성
        detailed_data = []
        for product in products:
            product_data = {
                'product_code': product.fin_prdt_cd,
                'bank_name': product.kor_co_nm,
                'product_name': product.fin_prdt_nm,
                'product_description': product.etc_note,
                'join_way': product.join_way,
                'join_deny': product.join_deny,
                'join_member': product.join_member,
                'max_limit': product.max_limit,
                'dcls_start_day': product.dcls_strt_day,
                'dcls_end_day': product.dcls_end_day,
                'options': [{
                    'save_term': option.save_trm,
                    'interest_rate_type': option.intr_rate_type,
                    'basic_rate': option.intr_rate,
                    'prime_rate': option.intr_rate2,
                    'reserve_type': option.rsrv_type
                } for option in product.options.all()]
            }
            detailed_data.append(product_data)
        
        return Response({
            'status': 'success',
            'message': '정기예금 상품 목록을 성공적으로 조회했습니다.',
            'total_count': len(detailed_data),
            'data': detailed_data
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'정기예금 상품 조회 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# DB에 저장된 모든 정기적금 상품 정보 조회 (단순 조회)
@api_view(['GET'])
def get_saving_products(request):
    try:
        products = SavingProduct.objects.all()
        
        # 각 상품의 상세 정보를 포함한 데이터 구성
        detailed_data = []
        for product in products:
            product_data = {
                'product_code': product.fin_prdt_cd,
                'bank_name': product.kor_co_nm,
                'product_name': product.fin_prdt_nm,
                'product_description': product.etc_note,
                'join_way': product.join_way,
                'join_deny': product.join_deny,
                'join_member': product.join_member,
                'max_limit': product.max_limit,
                'dcls_start_day': product.dcls_strt_day,
                'dcls_end_day': product.dcls_end_day,
                'fin_co_subm_day': product.fin_co_subm_day,
                'options': [{
                    'save_term': option.save_trm,
                    'interest_rate_type': option.intr_rate_type,
                    'basic_rate': option.intr_rate,
                } for option in product.options.all()]
            }
            detailed_data.append(product_data)
        
        return Response({
            'status': 'success',
            'message': '정기적금 상품 목록을 성공적으로 조회했습니다.',
            'total_count': len(detailed_data),
            'data': detailed_data
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'정기적금 상품 조회 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# import json
# import os

# url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
# params = {
#     "auth": settings.PROD_API_KEY,
#     "topFinGrpNo": "020000",  # 은행권 코드
#     "pageNo": "1"
# }

# response = requests.get(url, params=params)

# # JSON 데이터를 예쁘게 출력
# print(json.dumps(response.json(), indent=4, ensure_ascii=False))

# # JSON 파일로 저장
# with open('deposit_products.json', 'w', encoding='utf-8') as f:
#     json.dump(response.json(), f, indent=4, ensure_ascii=False)

# # 저장된 경로 출력
# print(f"파일이 저장된 경로: {os.path.abspath('deposit_products.json')}")


# url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
# params = {
#     "auth": settings.PROD_API_KEY,
#     "topFinGrpNo": "020000",  # 은행권 코드
#     "pageNo": "1"
# }

# response = requests.get(url, params=params)

# # JSON 데이터를 예쁘게 출력
# print(json.dumps(response.json(), indent=4, ensure_ascii=False))

# # JSON 파일로 저장
# with open('saving_products.json', 'w', encoding='utf-8') as f:
#     json.dump(response.json(), f, indent=4, ensure_ascii=False)

# # 저장된 경로 출력
# print(f"파일이 저장된 경로: {os.path.abspath('saving_products.json')}")
