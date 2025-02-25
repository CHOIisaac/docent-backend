from django.db import models

class Museum(models.Model):
    name = models.CharField(max_length=100, verbose_name='미술관/박물관명')
    address = models.CharField(max_length=200, verbose_name='주소')
    latitude = models.FloatField(null=True, blank=True, verbose_name='위도')
    longitude = models.FloatField(null=True, blank=True, verbose_name='경도')
    description = models.TextField(null=True, blank=True, verbose_name='설명')
    opening_hours = models.CharField(max_length=100, null=True, blank=True, verbose_name='운영시간')
    website = models.URLField(null=True, blank=True, verbose_name='웹사이트')
    image = models.ImageField(upload_to='museums/', null=True, blank=True, verbose_name='이미지')
    
    class Meta:
        db_table = 'museum'
        verbose_name = '미술관/박물관'
        verbose_name_plural = '미술관/박물관 목록'
    
    def __str__(self):
        return self.name

class Exhibition(models.Model):
    title = models.CharField(max_length=200, verbose_name='전시명')
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, related_name='exhibitions', verbose_name='미술관/박물관')
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(verbose_name='종료일')
    description = models.TextField(null=True, blank=True, verbose_name='전시 설명')
    poster = models.ImageField(upload_to='exhibitions/', null=True, blank=True, verbose_name='포스터')
    
    class Meta:
        db_table = 'exhibition'
        verbose_name = '전시'
        verbose_name_plural = '전시 목록'
    
    def __str__(self):
        return f"{self.title} - {self.museum.name}" 