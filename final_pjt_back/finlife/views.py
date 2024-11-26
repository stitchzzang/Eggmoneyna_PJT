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


@api_view(['GET'])
def get_economic_books(request):
    try:
        # 페이지 번호와 페이지당 도서 수를 요청에서 가져옴
        page = request.GET.get('page', 1)
        items_per_page = request.GET.get('items_per_page', 50)  # 기본값 50개로 증가
        
        try:
            page = int(page)
            items_per_page = min(int(items_per_page), 50)  # 최대 50개로 제한
        except ValueError:
            page = 1
            items_per_page = 50

        BASE_URL = "http://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
        params = {
            'TTBKey': settings.ALADIN_API_KEY,
            'QueryType': 'Keyword',
            'Query': '경제',
            'MaxResults': items_per_page,
            'start': page,  # 페이지 번호 적용
            'SearchTarget': 'Book',
            'Category': '170',
            'output': 'js',
            'Version': '20131101',
            'Sort': 'Salespoint'
        }

        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        books_data = response.json()

        if not books_data.get('item'):
            return Response({
                'status': 'error',
                'message': '검색 결과가 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)

        books = [{
            'title': item['title'],
            'author': item['author'],
            'publisher': item['publisher'],
            'pubDate': item['pubDate'],
            'cover': item['cover'],
            'description': item.get('description', '설명 없음'),
            'priceStandard': item['priceStandard'],
            'link': item['link'],
            'isbn13': item.get('isbn13', ''),
            'categoryName': item.get('categoryName', '')
        } for item in books_data['item']]

        return Response({
            'status': 'success',
            'message': '경제 도서 정보를 성공적으로 가져왔습니다.',
            'data': books
        })

    except requests.exceptions.RequestException as e:
        return Response({
            'status': 'error',
            'message': f'알라딘 API 요청 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'도서 정보 처리 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        result = data.get('result')
        
        if not result:
            return Response({
                'error': 'API 응답에 result 데이터가 없습니다.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        baseList = result.get('baseList')
        optionList = result.get('optionList')
        
        if not baseList or not optionList:
            return Response({
                'error': 'API 응답에 상품 데이터가 없습니다.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        saved_products = []
        for item in baseList:
            product, created = DepositProduct.objects.get_or_create(
                fin_prdt_cd=item['fin_prdt_cd'],
                defaults={
                    'dcls_month': item.get('dcls_month', ''),
                    'fin_co_no': item.get('fin_co_no', ''),
                    'kor_co_nm': item['kor_co_nm'],
                    'fin_prdt_nm': item['fin_prdt_nm'],
                    'join_way': item.get('join_way', ''),
                    'mtrt_int': item.get('mtrt_int', ''),
                    'spcl_cnd': item.get('spcl_cnd', ''),
                    'join_deny': item.get('join_deny', ''),
                    'join_member': item.get('join_member', ''),
                    'etc_note': item.get('etc_note', ''),
                    'max_limit': item.get('max_limit', None),
                    'dcls_strt_day': item.get('dcls_strt_day', ''),
                    'dcls_end_day': item.get('dcls_end_day', ''),
                    'fin_co_subm_day': item.get('fin_co_subm_day', '')
                }
            )
            
            if not created:
                for field in ['dcls_month', 'fin_co_no', 'kor_co_nm', 'fin_prdt_nm', 
                             'join_way', 'mtrt_int', 'spcl_cnd', 'join_deny', 
                             'join_member', 'etc_note', 'max_limit', 'dcls_strt_day',
                             'dcls_end_day', 'fin_co_subm_day']:
                    setattr(product, field, item.get(field, ''))
                product.save()
            
            # 기존 옵션 삭제
            product.options.all().delete()
            
            # 해당 상품의 옵션들 필터링
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
                    dcls_month=option.get('dcls_month', ''),
                    fin_co_no=option.get('fin_co_no', ''),
                    fin_prdt_cd=option['fin_prdt_cd'],
                    intr_rate_type=option.get('intr_rate_type', ''),
                    intr_rate_type_nm=option.get('intr_rate_type_nm', ''),
                    save_trm=save_trm,
                    intr_rate=intr_rate,
                    intr_rate2=float(option.get('intr_rate2', 0))
                )
                
                saved_options.append({
                    'id': saved_option.id,
                    'dcls_month': saved_option.dcls_month,
                    'fin_co_no': saved_option.fin_co_no,
                    'fin_prdt_cd': saved_option.fin_prdt_cd,
                    'intr_rate_type': saved_option.intr_rate_type,
                    'intr_rate_type_nm': saved_option.intr_rate_type_nm,
                    'save_trm': saved_option.save_trm,
                    'intr_rate': saved_option.intr_rate,
                    'intr_rate2': saved_option.intr_rate2
                })
            
            saved_products.append({
                'id': product.id,
                'dcls_month': product.dcls_month,
                'fin_co_no': product.fin_co_no,
                'fin_prdt_cd': product.fin_prdt_cd,
                'kor_co_nm': product.kor_co_nm,
                'fin_prdt_nm': product.fin_prdt_nm,
                'join_way': product.join_way,
                'mtrt_int': product.mtrt_int,
                'spcl_cnd': product.spcl_cnd,
                'join_deny': product.join_deny,
                'join_member': product.join_member,
                'etc_note': product.etc_note,
                'max_limit': product.max_limit,
                'dcls_strt_day': product.dcls_strt_day,
                'dcls_end_day': product.dcls_end_day,
                'fin_co_subm_day': product.fin_co_subm_day,
                'options': saved_options
            })
        
        return Response({
            'status': 'success',
            'message': '정기예금 데이터 저장완료',
            'data': {
                'count': len(saved_products),
                'products': saved_products
            }
        })
        
    except requests.exceptions.RequestException as e:
        return Response({
            'status': 'error',
            'message': f'API 요청 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'데이터 처리 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                'dcls_month': item.get('dcls_month', ''),
                'fin_co_no': item.get('fin_co_no', ''),
                'kor_co_nm': item['kor_co_nm'],
                'fin_prdt_nm': item['fin_prdt_nm'],
                'join_way': item.get('join_way', ''),
                'mtrt_int': item.get('mtrt_int', ''),
                'spcl_cnd': item.get('spcl_cnd', ''),
                'join_deny': item.get('join_deny', ''),
                'join_member': item.get('join_member', ''),
                'etc_note': item.get('etc_note', ''),
                'max_limit': item.get('max_limit', None),
                'dcls_strt_day': item.get('dcls_strt_day', ''),
                'dcls_end_day': item.get('dcls_end_day', ''),
                'fin_co_subm_day': item.get('fin_co_subm_day', '')
            }
        )
        
        if not created:
            # 모든 필드 업데이트
            for field in ['dcls_month', 'fin_co_no', 'kor_co_nm', 'fin_prdt_nm', 
                         'join_way', 'mtrt_int', 'spcl_cnd', 'join_deny', 
                         'join_member', 'etc_note', 'max_limit', 'dcls_strt_day',
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
                dcls_month=option.get('dcls_month', ''),
                fin_prdt_cd=option['fin_prdt_cd'],
                intr_rate_type=option.get('intr_rate_type', ''),
                intr_rate=intr_rate,
                save_trm=save_trm,
                intr_rate_type_nm=option.get('intr_rate_type_nm', ''),
                intr_rate2=float(option.get('intr_rate2', 0)),
                rsrv_type=option.get('rsrv_type', ''),
                rsrv_type_nm=option.get('rsrv_type_nm', '')
            )
            
            saved_options.append({
                'fin_prdt_cd': saved_option.fin_prdt_cd,
                'intr_rate_type': saved_option.intr_rate_type,
                'intr_rate_type_nm': saved_option.intr_rate_type_nm,
                'rsrv_type': saved_option.rsrv_type,
                'rsrv_type_nm': saved_option.rsrv_type_nm,
                'save_trm': saved_option.save_trm,
                'intr_rate': saved_option.intr_rate,
                'intr_rate2': saved_option.intr_rate2,
            })
        
        saved_products.append({
            'id': product.id,
            'dcls_month': product.dcls_month,
            'fin_co_no': product.fin_co_no,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'join_way': product.join_way,
            'mtrt_int': product.mtrt_int,
            'spcl_cnd': product.spcl_cnd,
            'join_deny': product.join_deny,
            'join_member': product.join_member,
            'etc_note': product.etc_note,
            'max_limit': product.max_limit,
            'dcls_strt_day': product.dcls_strt_day,
            'dcls_end_day': product.dcls_end_day,
            'fin_co_subm_day': product.fin_co_subm_day,
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
        serializer = DepositProductSerializer(products, many=True)
        
        return Response({
            'status': 'success',
            'message': '정기적금 상품 목록을 성공적으로 조회했습니다.',
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'정기적금 상품 조회 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# DB에 저장된 모든 정기적금 상품 정보 조회 (단순 조회)
@api_view(['GET'])
def get_saving_products(request):
    try:
        products = SavingProduct.objects.all()
        serializer = SavingProductSerializer(products, many=True)
        
        return Response({
            'status': 'success',
            'message': '정기적금 상품 목록을 성공적으로 조회했습니다.',
            'data': serializer.data
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
