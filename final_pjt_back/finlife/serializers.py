from rest_framework import serializers
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption

class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = [
            'id',
            'dcls_month',
            'fin_co_no',
            'fin_prdt_cd',
            'intr_rate_type',
            'intr_rate_type_nm',
            'save_trm',
            'intr_rate',
            'intr_rate2',
        ]

class DepositProductSerializer(serializers.ModelSerializer):
    options = DepositOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = DepositProduct
        fields = [
            'id',
            'dcls_month',
            'fin_co_no',
            'fin_prdt_cd',
            'kor_co_nm',
            'fin_prdt_nm',
            'join_way',
            'mtrt_int',
            'spcl_cnd',
            'join_deny',
            'join_member',
            'etc_note',
            'max_limit',
            'dcls_strt_day',
            'dcls_end_day',
            'fin_co_subm_day',
            'options',
        ]

class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = [
            'id',
            'product',
            'dcls_month',
            'fin_prdt_cd',
            'intr_rate_type',
            'intr_rate',
            'save_trm',
            'intr_rate_type_nm',
            'intr_rate2',
            'rsrv_type',
            'rsrv_type_nm',
        ]

class SavingProductSerializer(serializers.ModelSerializer):
    options = SavingOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = SavingProduct
        fields = [
            'id',
            'dcls_month',
            'fin_co_no',
            'fin_prdt_cd',
            'kor_co_nm',
            'fin_prdt_nm',
            'join_way',
            'mtrt_int',
            'spcl_cnd',
            'join_deny',
            'join_member',
            'etc_note',
            'max_limit',
            'dcls_strt_day',
            'dcls_end_day',
            'fin_co_subm_day',
            'options',
        ]