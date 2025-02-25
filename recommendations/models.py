from django.db import models
from accounts.models import User
from artworks.models import Artwork
from museums.models import Museum, Exhibition

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences', verbose_name='사용자')
    artwork_style = models.CharField(max_length=100, null=True, blank=True, verbose_name='선호 작품 스타일')
    artist = models.CharField(max_length=100, null=True, blank=True, verbose_name='선호 작가')
    
    class Meta:
        db_table = 'user_preference'
        verbose_name = '사용자 선호도'
        verbose_name_plural = '사용자 선호도 목록'

class UserArtworkInteraction(models.Model):
    INTERACTION_TYPES = (
        ('view', '조회'),
        ('like', '좋아요'),
        ('bookmark', '북마크'),
        ('comment', '댓글'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artwork_interactions', verbose_name='사용자')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='user_interactions', verbose_name='작품')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES, verbose_name='상호작용 유형')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    
    class Meta:
        db_table = 'user_artwork_interaction'
        verbose_name = '사용자-작품 상호작용'
        verbose_name_plural = '사용자-작품 상호작용 목록'

class UserMuseumInteraction(models.Model):
    INTERACTION_TYPES = (
        ('view', '조회'),
        ('visit', '방문'),
        ('bookmark', '북마크'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='museum_interactions', verbose_name='사용자')
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, related_name='user_interactions', verbose_name='미술관/박물관')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES, verbose_name='상호작용 유형')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    
    class Meta:
        db_table = 'user_museum_interaction'
        verbose_name = '사용자-미술관 상호작용'
        verbose_name_plural = '사용자-미술관 상호작용 목록' 