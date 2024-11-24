from rest_framework import serializers
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption

class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'

class DepositProductSerializer(serializers.ModelSerializer):
    depositoptions = DepositOptionSerializer(many=True, read_only=True)
    dcls_month = serializers.SerializerMethodField()
    
    class Meta:
        model = DepositProduct
        fields = [
            'id',
            'fin_prdt_cd',
            'kor_co_nm',
            'fin_prdt_nm',
            'etc_note',
            'join_way',
            'join_deny',
            'join_member',
            'max_limit',
            'dcls_strt_day',
            'dcls_end_day',
            'dcls_month',
            'fin_co_subm_day',
            'depositoptions',
        ]
    
    def get_dcls_month(self, obj):
        if obj.dcls_strt_day:
            try:
                return obj.dcls_strt_day[2:6]
            except:
                return None
        return None

class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = (
            'id', 
            'product',
            'fin_prdt_cd', 
            'intr_rate_type', 
            'intr_rate', 
            'save_trm',
            'created_at',
            'updated_at'
        )

class SavingProductSerializer(serializers.ModelSerializer):
    options = SavingOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = SavingProduct
        fields = '__all__'