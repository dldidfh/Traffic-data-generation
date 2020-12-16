from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from Demacia.storage_backends import PublicMediaStorage, StaticStorage

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length = 50, verbose_name='아이디',primary_key=True)
    password = models.CharField(max_length = 50, verbose_name='비밀번호')
    name = models.CharField(max_length=20, verbose_name='사용자명')
    
class Admin(models.Model):
    admin_id = models.CharField(max_length = 50, verbose_name='관리자 아이디',primary_key=True)
    password = models.CharField(max_length = 50, verbose_name='관리자 비밀번호')
    name = models.CharField(default="관리자" ,max_length=20, verbose_name='관리자 이름')

class VideoFile(models.Model):
    id  = models.AutoField(verbose_name="id", primary_key=True)
    user_id = models.ForeignKey(User,db_column="user_id", on_delete=models.CASCADE)
    # upload_file = models.FileField(upload_to='upload_video', verbose_name='파일이름', unique=True)
    upload_file = models.FileField(storage=PublicMediaStorage(), upload_to='upload_video/video', verbose_name='파일이름', unique=True)
    uploaded_time = models.DateTimeField(auto_now_add=True, verbose_name='시간')
    state = models.IntegerField(default=0, verbose_name='상태')
    csv_file = models.FileField(storage=PublicMediaStorage(),upload_to='upload_video/csv', verbose_name='csv파일', unique=False)
    convert_file = models.FileField(storage=PublicMediaStorage(), upload_to='upload_video/converted_video', verbose_name="분석영상", unique=False)    
    # 라인긋기 데이터 저장
    line_data = models.TextField(verbose_name='선데이터', null=True)

class TrafficCount(models.Model):
    file_name = models.CharField(max_length = 100, verbose_name='파일이름')
    date = models.DateTimeField(auto_now_add=True, verbose_name='날짜', null=False)
    time = models.TimeField(auto_now_add=True, verbose_name='시간', null=False)
    total = models.IntegerField(verbose_name='교통량총계')
    straight = models.IntegerField(verbose_name='직진')
    turn_left = models.IntegerField(verbose_name='좌회전')
    turn_right = models.IntegerField(verbose_name='우회전')

class SeoulPlaza(models.Model):
    id  = models.AutoField(verbose_name="id", primary_key=True)
    intersection_name = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    month = models.TextField(blank=True, null=True)
    day = models.TextField(blank=True, null=True)
    hour = models.TextField(blank=True, null=True)
    min = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

class SeoulPlaza_Night(models.Model):
    id  = models.AutoField(verbose_name="id", primary_key=True)
    intersection_name = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    month = models.TextField(blank=True, null=True)
    day = models.TextField(blank=True, null=True)
    hour = models.TextField(blank=True, null=True)
    min = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

class Cheonggye_6_ga(models.Model):
    id  = models.AutoField(verbose_name="id", primary_key=True)
    intersection_name = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    month = models.TextField(blank=True, null=True)
    day = models.TextField(blank=True, null=True)
    hour = models.TextField(blank=True, null=True)
    min = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

class Cheonggye_6_ga_Night(models.Model):
    id  = models.AutoField(verbose_name="id", primary_key=True)
    intersection_name = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    month = models.TextField(blank=True, null=True)
    day = models.TextField(blank=True, null=True)
    hour = models.TextField(blank=True, null=True)
    min = models.TextField(blank=True, null=True)
    frame = models.TextField(blank=True, null=True)
    direction_1 = models.IntegerField(blank=True, null=True)
    direction_2 = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)

