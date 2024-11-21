from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from datetime import datetime


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
