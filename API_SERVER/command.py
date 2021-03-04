import os
# import datetime
import time
import threading
from datetime import datetime
from pathlib import Path

# while True:
# save_file_name = ['test.mkv', 'test2.mkv', 'test3.mkv', '영상데이터/test4.mkv']
# for text in save_file_name:
def model_convertion(date_str, name_list):
    # time.sleep(300)
    dir_cctv_data = 'cctv_data/'
    dir_converted_data = "converted_cctv_data/"
    # converted_file_name = dir_converted_data + date_str
    # f = open(converted_file_name, 'w')
    # f.close()

    delete_old_files(dir_cctv_data + name_list)
    # delete_old_files(dir_converted_data)

def delete_old_files(path_target):
    start = time.time()
    """path_target:삭제할 파일이 있는 디렉토리, days_elapsed:경과일수"""
    for f in os.listdir(path_target): # 디렉토리를 조회한다
        f = os.path.join(path_target, f)
        print('파일 이름 : ',f)
        if os.path.isfile(f): # 파일이면
            timestamp_now = datetime.now().timestamp() # 타임스탬프(단위:초)
            # st_mtime(마지막으로 수정된 시간)기준 X일 경과 여부
            is_old = os.stat(f).st_mtime < timestamp_now - ( 24 * 60 * 60)
            if is_old: # 1일 경과했다면
                try:
                    os.remove(f) # 파일을 지운다
                    print(f, 'is deleted') # 삭제완료 로깅
                except OSError: # Device or resource busy (다른 프로세스가 사용 중)등의 이유
                    print(f, 'can not delete') # 삭제불가 로깅
            else: print("기간내 파일 없음")
    end = time.time()
    print(f'파일 삭제 경과 시간: {end-start}')

def crawl(url, name):
    now = time.localtime()
    date_str =str(now.tm_year) + '_' + str(now.tm_mon) + '_' + str(now.tm_mday) + '_' + str(now.tm_hour) + '_' +  str(now.tm_min) + '_' +  str(now.tm_sec) + '.mkv'
    Path("cctv_data/"+name + '/').mkdir(parents=True, exist_ok=True)
    folder_path = 'cctv_data/' + name + '/'
    start = time.time()
    os.system(
        'ffmpeg -y -loglevel warning -i   '+ url + ' -t 30 -pix_fmt yuv420p  -codec copy -r 30 '+ folder_path + name+ '_' + date_str
        )
    
    end = time.time()
    print(name,'\t경과 시간 : ',end - start)

url_list = [
        "url1", # 서울시청
        "url2", # 서울광장
        "url3", # 신촌
        "url4", # 퇴계2가
        "url5", # 청계6가
        "url6", #약수고가
        "url7",  # 공덕오거리
        "url8",  # 영동전화국
        "url9",  # 이수역
        "url10",   # 수락지하도 - 테스트용
        'url11',  # 신영삼거리
        'url12',  # 장충로터리
        "url13"   # 잠실한강공원
    ]
name_list = [
        'Seoul_City_Hall',
        'Seoul_Plaza',
        'Sinchon',
        'Toegye_2_ga',
        'Cheonggye_6_ga',
        'yagsu_Overpass',
        'Gongdeok_5_way',
        'Yeongdong_Telephone_Office',
        'Esu_Station',
        'SuRak_Underpass',
        'Sinyoung_3_way',
        'Jangchung_Rotary',
        'Jamsil_Han_River_Park'
    ]

while True:
# for i in range(1):
    now = time.localtime()
    date_str =str(now.tm_year) + '_' + str(now.tm_mon) + '_' + str(now.tm_mday) + '_' + str(now.tm_hour) + '_' +  str(now.tm_min) + '_' +  str(now.tm_sec) + '.mkv'
    # if now.tm_hour == 1 or now.tm_hour == 2 or now.tm_hour == 3 or now.tm_hour == 4 or now.tm_hour == 5 or now.tm_hour == 6 or now.tm_hour == 7 or now.tm_hour == 8 or now.tm_hour == 9 :
    # if now.tm_hour == 18 or now.tm_hour == 19 or now.tm_hour == 20 or now.tm_hour == 21 or now.tm_hour == 22 or now.tm_hour == 23 or now.tm_hour == 0 :
    # if now.tm_hour == 18 or now.tm_hour == 19 or now.tm_hour == 20 or now.tm_hour == 21 or now.tm_hour == 22 or now.tm_hour == 23 or now.tm_hour == 0 :
    
    # if now.tm_min == 25 : 
    for i in range(len(url_list)):
        
        date_str =str(now.tm_year) + '_' + str(now.tm_mon) + '_' + str(now.tm_mday) + '_' + str(now.tm_hour) + '_' +  str(now.tm_min) + '_' +  str(now.tm_sec) + '.mkv'
        t2 = threading.Thread(target=crawl, args=(url_list[i], name_list[i]))
        t2.start()
        t = threading.Thread(target=model_convertion, args=(date_str,name_list[i]))
        t.start()

    time.sleep(3000)
    
    # print(now)
