from django.db import models

class DepositProduct(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_nm = models.TextField()  # 금융상품명
    etc_note = models.TextField()  # 금융상품설명
    join_way = models.TextField()  # 가입방법
    join_deny = models.TextField()  # 가입제한
    join_member = models.TextField()  # 가입대상
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()  # 금융상품코드
    intr_rate_type = models.TextField()  # 금리유형
    intr_rate = models.FloatField()  # 금리
    save_trm = models.IntegerField()  # 저축기간
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SavingProduct(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_nm = models.TextField()  # 금융상품명
    etc_note = models.TextField()  # 금융상품설명
    join_way = models.TextField()  # 가입방법
    join_deny = models.TextField()  # 가입제한
    join_member = models.TextField()  # 가입대상
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SavingOption(models.Model):
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()  # 금융상품코드
    intr_rate_type = models.TextField()  # 금리유형
    intr_rate = models.FloatField()  # 금리
    save_trm = models.IntegerField()  # 저축기간
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
