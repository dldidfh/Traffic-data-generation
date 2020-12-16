from django.db import models
from django.conf import settings
from testproject.storage_backends import PublicMediaStorage, StaticStorage

class DemaciaappUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'DemaciaApp_user'
class DemaciaappVideofile(models.Model):
    upload_file = models.CharField(unique=True, max_length=100)
    uploaded_time = models.DateTimeField()
    state = models.IntegerField() # 0 진행중 1 모델분석시작 2 완료 
    csv_file = models.CharField(max_length=100)
    user = models.ForeignKey(DemaciaappUser, models.DO_NOTHING)
    line_data = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'DemaciaApp_videofile'