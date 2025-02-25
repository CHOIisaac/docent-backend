from django.db import models
from museums.models import Museum

class Artist(models.Model):
    name = models.CharField(max_length=100, verbose_name='작가명')
    birth_year = models.IntegerField(null=True, blank=True, verbose_name='출생연도')
    death_year = models.IntegerField(null=True, blank=True, verbose_name='사망연도')
    nationality = models.CharField(max_length=50, null=True, blank=True, verbose_name='국적')
    description = models.TextField(null=True, blank=True, verbose_name='작가 설명')
    
    class Meta:
        db_table = 'artist'
        verbose_name = '작가'
        verbose_name_plural = '작가 목록'
    
    def __str__(self):
        return self.name

class Artwork(models.Model):
    title = models.CharField(max_length=200, verbose_name='작품명')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artworks', verbose_name='작가')
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, related_name='artworks', verbose_name='소장 미술관')
    year = models.IntegerField(null=True, blank=True, verbose_name='제작연도')
    description = models.TextField(null=True, blank=True, verbose_name='작품 설명')
    image = models.ImageField(upload_to='artworks/', null=True, blank=True, verbose_name='작품 이미지')
    style = models.CharField(max_length=100, null=True, blank=True, verbose_name='작품 스타일')
    medium = models.CharField(max_length=100, null=True, blank=True, verbose_name='매체')
    dimensions = models.CharField(max_length=100, null=True, blank=True, verbose_name='크기')
    
    class Meta:
        db_table = 'artwork'
        verbose_name = '작품'
        verbose_name_plural = '작품 목록'
    
    def __str__(self):
        return f"{self.title} - {self.artist.name}"

class ArtworkTag(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='tags', verbose_name='작품')
    name = models.CharField(max_length=50, verbose_name='태그명')
    
    class Meta:
        db_table = 'artwork_tag'
        verbose_name = '작품 태그'
        verbose_name_plural = '작품 태그 목록'
    
    def __str__(self):
        return f"{self.artwork.title} - {self.name}" 