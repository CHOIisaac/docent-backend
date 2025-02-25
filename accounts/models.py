from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    SOCIAL_CHOICES = (
        ('kakao', '카카오'),
        ('google', '구글'),
        ('naver', '네이버'),
    )
    
    social_provider = models.CharField(max_length=20, choices=SOCIAL_CHOICES, null=True, blank=True)
    social_id = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.URLField(null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록' 