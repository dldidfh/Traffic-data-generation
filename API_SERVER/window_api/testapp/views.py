from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
import os, json
from django.shortcuts import get_object_or_404
import subprocess
import threading
from pathlib import Path
from django.http import HttpResponse
from django.http import JsonResponse
import re
import time
from .models import DemaciaappVideofile 
# Create your views here.
def test(request):
    print('IP : \t', request.META.get('REMOTE_ADDR'))
    return render(request, 'test.html')
def file_info(request):
    file_id  = request.GET.get('id',None)
    print('IP : \t', request.META.get('REMOTE_ADDR'))
    if file_id != None:
        file_list = DemaciaappVideofile.objects.get(id=file_id) 
        uploaded_file = file_list.upload_file
        line_data = file_list.line_data
        line_data = re.findall('\d+',line_data)
        for i in range(0, len(line_data)): 
            line_data[i] = int(line_data[i])
        line_data = str(line_data).replace(' ', '')

        # print('변환 후 ',line_data)
        # download_s3(uploaded_file,line_data)
        t2 = threading.Thread(target=download_s3, args=(uploaded_file, str(line_data)))
        t2.start()
    return render(request,'test.html')


def download_s3(uploaded_file, line_data):
    # uploaded_file 형식 : upload_video/video/test.mkv
    # 디렉토리 생성을 위한 경로 생성
    split_uploaded_file_path = os.path.split(uploaded_file)
    uploaded_file_directory_path = split_uploaded_file_path[0] + '/'    # upload_video/video/
    uploaded_file_only_file_name = split_uploaded_file_path[1]          # test.mkv
    
    # 원본파일 저장 위치
    local_origin_file_directory_path = 'upload_origin_video/' + uploaded_file_directory_path 
    local_origin_file_path = 'upload_origin_video/' + uploaded_file
    # 모델 변환 파일 저장위치
    local_converted_file_directory_path = 'upload_converted_video/' + uploaded_file_directory_path 
    local_converted_file_path = 'upload_converted_video/' + uploaded_file_directory_path + 'converted_' + uploaded_file_only_file_name

    # 저장을 위한 디렉토리 생성
    Path(local_converted_file_directory_path).mkdir(parents=True, exist_ok=True)
    Path(local_origin_file_directory_path).mkdir(parents=True, exist_ok=True)
    

    # DB에서 파일 명을 가져와서 S3에 저장되있는 영상 파일 다운로드
    subprocess.check_call('aws s3 cp s3://demacia-s3-second/' + uploaded_file + ' ' + local_origin_file_directory_path  , shell=True)
    # 모델에 적용
    start = time.time()
    subprocess.check_call('python object_tracker.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --video ' + local_origin_file_path + ' --output ' + local_converted_file_path + ' --user_upload ' + line_data, shell=True)
    local_origin_file_path = local_origin_file_path.replace('/', '\\')
    local_converted_file_path = local_converted_file_path.replace('/', '\\')

    end = time.time()
    print('끝 \t',round((end-start)/60,5))


