from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .forms import VideoUploadForm
import json
import os
from django.db.models import Count, Max
from .models import User, Admin, VideoFile, TrafficCount, SeoulPlaza,Cheonggye_6_ga ,SeoulPlaza_Night,Cheonggye_6_ga_Night
import socket
from struct import pack
import requests
import boto3
from django.db.models import Max , Sum,F
import datetime, time

# import httplib, json, datetime

INGEST_LIST="/druid/indexer/v1/tasks"
# Create your views here.

def main(request):
    print("메인페이지")
    session = request.session.get('user_id')
    return render(request, 'Home.html') 

# 로그인
def login(request):
    print("로그인")
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id',None)
        password = request.POST.get('password',None)
        isCheck = request.POST.get('isCheck',None)
        print("isCheck",isCheck)
        customer = {}
        if isCheck == 'true':
            print("어드민 로긴 접근")
            try:
                model_admin = Admin.objects.get(admin_id=user_id)
                if model_admin.password == password:
                    # session_id = request.session.session_key
                    request.session['user_id'] = model_admin.admin_id
                    customer['check']='admin_yes'
                    # customer['session_id'] = session_id
                    # customer['session'] = session
                else:
                    customer['check']='admin_nopassword'
                    request.session['user_id'] = False
            except Admin.DoesNotExist:
                customer['check']='admin_no'
                request.session['user_id'] = False

            print("customer",customer)
            return HttpResponse(json.dumps(customer), content_type="application/json")

        else:
            print("유저로긴 접근")
            try:
                if user_id != 'demacia':
                    model_user = User.objects.get(user_id=user_id)
                    if model_user.password == password:
                        # session_id = request.session.session_key
                        request.session['user_id'] = model_user.user_id
                        customer['check']='yes'
                        # customer['session_id'] = session_id
                        # customer['session'] = session
                    else:
                        customer['check']='nopassword'
                        request.session['user_id'] = False
                else:
                    customer['check']='admin_no'
                    request.session['user_id'] = False

            except User.DoesNotExist:
                customer['check']='no'
                request.session['user_id'] = False
                
            print("customer",customer)
            return HttpResponse(json.dumps(customer), content_type="application/json")


# 회원가입
def user_regist(request):
    print("회원가입")
    if request.method =='GET':
        return render(request, 'user_regist.html')

    if request.method == 'POST':
        user_id = request.POST.get('user_id',None)
        password = request.POST.get('password',None)
        name = request.POST.get('user_name',None)
        print("name",name)
        user = User(user_id=user_id,password=password,name=name)
        user.save()
        return render(request, 'Home.html' )

# 중복체크
def user_id_check(request):

    if request.method == 'POST':
        user_id = request.POST.get('user_id',None)
        try:
            user = User.objects.get(user_id=user_id)
            check = {'check':'yes'}
        except User.DoesNotExist:
            check = {'check':'no'}
        
        return HttpResponse(json.dumps(check), content_type="application/json")

# 로그아웃
def logout(request):
    request.session.pop('user_id')
    return render(request,'Home.html')

# 마이페이지
def mypage(request):
    session = request.session.get('user_id')

    print("유저 세션 아이디", session)
    if session != 'demacia':
        user = User.objects.get(user_id=session)
        user_dict = {}
        user_dict['user_id'] = user.user_id
        user_dict['password'] = user.password
        user_dict['name'] = user.name
    else:
        admin = Admin.objects.get(admin_id=session)
        user_dict = {}
        user_dict['user_id'] = admin.admin_id
        user_dict['password'] = admin.password
        user_dict['name'] = admin.name
    print(user_dict)
    return render(request,'mypage.html', user_dict)  

# 교통분석의뢰 페이지이동
def video_analysis(request):
    session = request.session.get('user_id')

    if session:
        return render(request,'video_analysis.html')
    else:
        return render(request,'error.html')

# 파일 업로드
def file_upload(request):
    if request.method =='POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("실패")

        return render(request,'video_analysis.html')

    return render(request,'video_analysis.html')

# 요청 리스트
def request_list(request):
    session = request.session.get('user_id')
    if session:
        request_list = VideoFile.objects.filter(user_id=session).order_by('-uploaded_time')
        paginator = Paginator(request_list,7)
        page = request.GET.get('page')
        print("page",page)
        posts = paginator.get_page(page)
        print("request_list",request_list)
        return render(request,'request_list.html',{"posts": posts})
    else:
        return render(request,'error.html')


# 교통정보
def traffic_volume_research(request):
    session = request.session.get('user_id')
    if session:
        return render(request,'traffic_volume_research.html')
    else:
        return render(request,'error.html')

# 교통정보 테이블 데이터 가져오기
def traffic_volumne_research_data(request):
    if request.method =='POST':
        session = request.session.get('user_id')
        sign = request.POST.get('sign')
        frame = request.POST.get('frame')
        if session:
            direction1 = []
            direction2 = []
            result_direction = []
            info = []
            now = time.localtime()
            now_year = now.tm_year
            now_month = now.tm_mon
            now_day = now.tm_mday
            now_hour = now.tm_hour
            now_min = now.tm_min
            chart_car = []
            chart_bus = []
            chart_truck = []
            chart_hour = []
            chart_min = []
            temp_bus=0
            temp_car=0
            temp_truck=0

            # 클래스 가져오기
            db_table = f(sign) 
            db_table_data = db_table.objects.all()
           
            for data in db_table_data:
                direction1.append(data.direction_1)

            # 방향 데이터 리스트로 변환
            set_direction_1 =  set(direction1)
            list_direction = []
            for i in set_direction_1:
                list_direction.append(i) # direction 1 에대한 리스트

            # direction 값 넘기기
            for data in list_direction: # direction_1에 대한 반복문
                filteredList = list(filter(lambda x: x!=data, list_direction))
                for data2 in filteredList: # direction_2에 대한 반복문
                    object_loop1 = db_table.objects.filter(frame=frame, direction_1=data, direction_2=data2)
                    sum_car = sum_bus = sum_truck = sum_total = 0
                    for data3 in object_loop1: # car, bus, truck의 합계 저장
                        # print("데이타3",data3)
                        sum_car += data3.car
                        sum_bus += data3.bus
                        sum_truck += data3.truck
                        sum_total += data3.car+data3.bus+data3.truck

                    info.append({
                        'direction1': data,
                        'direction2':data2,
                        'bus': sum_bus,
                        'car': sum_car,
                        'truck':  sum_truck ,
                        'total': sum_total
                    })
        
            return render(request,'traffic_volume_research_ajax.html',{'info':info} )
            # return HttpResponse(json.dumps(info), content_type="application/json")
        else:
            pass
    else:
        return render(request,'traffic_volumne_research.html')


def f(x):
    return {'0':SeoulPlaza,'1':SeoulPlaza_Night,'2':Cheonggye_6_ga,'3':Cheonggye_6_ga_Night}[x]

# 차트 데이터 뽑기
def traffic_volumne_research_chart_data(request):
    if request.method =='POST':
        session = request.session.get('user_id')
        sign = request.POST.get('sign')
        frame = request.POST.get('frame')
        if session:
            chart_car = []
            chart_bus = []
            chart_truck = []
            chart_hour = []
            chart_min = []

            # 클래스 가져오기
            db_table = f(sign) 
            db_table_data = db_table.objects.filter(frame__lte=frame).values('frame').annotate(hour_val=F('hour'),min_val=F('min'),car_sum=Sum('car'),bus_sum=Sum('bus'),truck_sum=Sum('truck'))
            
            for value in db_table_data:
                chart_hour.append(value['hour_val'])
                chart_min.append(value['min_val'])
                chart_bus.append(value['bus_sum'])
                chart_car.append(value['car_sum'])
                chart_truck.append(value['truck_sum'])

            chart_dict = {
                'hour':chart_hour,
                'min':chart_min,
                'bus':chart_bus,
                'car':chart_car,
                'truck':chart_truck
            }

            # return render(request,'traffic_volume_research_chart_ajax.html',{'chart_dict':chart_dict} )
            return HttpResponse(json.dumps(chart_dict), content_type="application/json")
        else:
            pass
    else:
        return render(request,'traffic_volumne_research.html')


# 관리자 대쉬보드
def admin_home(request):
    session = request.session.get('user_id')
    print("session",session)
    video_all_count = VideoFile.objects.count()
    video_true_count = VideoFile.objects.filter(state=True).count() 
    video_false_count = VideoFile.objects.filter(state=False).count()
    user_all_count = User.objects.count()

    most_req_user = VideoFile.objects.values('user_id').annotate(max_count=Count('id')).values('user_id','max_count').order_by('-max_count')
    data = {
        'video_all_count' : video_all_count,
        'video_false_count' : video_false_count,
        'video_true_count' : video_true_count,
        'most_req_user' : most_req_user[0]['user_id'],
        'most_req_user_count' : most_req_user[0]['max_count'],
        'user_all_count' : user_all_count

    }
    return render(request, 'admin_home.html', {'data' : data})

def admin_video_list(request):
    
    session = request.session.get('user_id')
    if session == 'demacia':
        request_list = VideoFile.objects.filter(state=False).order_by('-uploaded_time')
        paginator = Paginator(request_list,15)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    return render(request, 'admin_video_list.html', {'posts': posts})

def image_popup(request):
    session = request.session.get('user_id')
    file_name = request.POST.get('file_name',None)
    return render(request, 'image_popup copy.html', {'file_name':file_name})

def video_analysis_progress(request):

    file_name = request.POST.get('file_name',None)
    line_list = request.POST.getlist('line_list')

    post_list = VideoFile.objects.get(upload_file=file_name)
    post_list.line_data=line_list
    post_list.save()
    params = {'id':post_list.id}
    result = requests.get('IP', params=params) #request.GET  
    if result.status_code == 200:
        
        print("접속 성공")
        video_file_list = VideoFile.objects.get(upload_file=file_name)
        video_file_list.state = 1
        video_file_list.save()
    else:
        print("접속 실패")


    return HttpResponse(json.dumps('성공'), content_type="application/json")