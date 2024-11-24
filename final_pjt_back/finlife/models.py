from django.db import models

class DepositProduct(models.Model):
    dcls_month = models.CharField(max_length=6)  # 공시 제출월
    fin_co_no = models.CharField(max_length=10)  # 금융회사 코드
    fin_prdt_cd = models.CharField(max_length=50)  # 금융상품 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)  # 상품명
    join_way = models.CharField(max_length=100)  # 가입방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대조건
    join_deny = models.CharField(max_length=1)  # 가입제한
    join_member = models.TextField()  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.BigIntegerField(null=True)  # 최고한도
    dcls_strt_day = models.CharField(max_length=8)  # 공시 시작일
    dcls_end_day = models.CharField(max_length=8, null=True)  # 공시 종료일
    fin_co_subm_day = models.CharField(max_length=8)  # 금융회사 제출일

class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    dcls_month = models.CharField(max_length=6)
    fin_co_no = models.CharField(max_length=10)
    fin_prdt_cd = models.CharField(max_length=50)
    intr_rate_type = models.CharField(max_length=1)
    intr_rate_type_nm = models.CharField(max_length=10)
    save_trm = models.IntegerField()
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    rsrv_type = models.CharField(max_length=100, blank=True)

class SavingProduct(models.Model):
    dcls_month = models.CharField(max_length=6)  # 공시 제출월
    fin_co_no = models.CharField(max_length=20)  # 금융회사 코드
    fin_prdt_cd = models.CharField(max_length=100)  # 금융상품 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)  # 상품명
    join_way = models.TextField()  # 가입방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대조건
    join_deny = models.CharField(max_length=1)  # 가입제한 (1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.BigIntegerField(null=True)  # 최대 한도
    dcls_strt_day = models.CharField(max_length=8)  # 공시 시작일
    dcls_end_day = models.CharField(max_length=8, null=True)  # 공시 종료일
    fin_co_subm_day = models.CharField(max_length=8)  # 금융회사 제출일

class SavingOption(models.Model):
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='options')
    dcls_month = models.CharField(max_length=6)
    fin_prdt_cd = models.TextField()  # 금융상품코드
    intr_rate_type = models.TextField()  # 금리유형
    intr_rate = models.FloatField()  # 금리
    save_trm = models.IntegerField()  # 저축기간

