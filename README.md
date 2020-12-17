## 모델 실행 방법

    1. Detecting 모델에서 가중치 생성
    2. 생성된 가중치 파일 'data' 폴더에 넣기
    3. python save_model.py -- weights ./data/'생성한 가중치 파일'.weights --output ./checkpoints/yolov4-416 --input_size 416 --model yolov4
    4. python object_tracker.py --video ./data/video/'test'.mp4 --output ./outputs/'demo'.avi --model yolov4
    *이렇게 하면 분석 영상 파일명 : 'test', 최종 분석 파일명 : 'demo'*
    5. 'count', 'location' 플래그를 사용하여 원하는 기능 추가 가능

## YOLO v4 사용 방법

[바로가기](https://gitlab.com/seoungjun_kim/test1)

## Ubuntu + Nginx 로 로드밸런싱 구현한 방법

1. 우분투에서 nginx 설치

2. 패키지 설치 완료 후 /etc/nginx/sites-available 디렉토리로 이동

3. sudo vi default 명령어로 파일 생성 후 아래와 같이 작성

'''
upstream myserver{
        server 49.50.165.14:80;
        server 27.96.130.138:80;
        server 101.101.217.200:8080;
        keepalive 100;    # keepalive 로 유지시키는 최대 커넥션 개수
}

server {
        listen 80;
        listen 443 ssl;

        location / {
                proxy_pass http://myserver;
        }
}

'''

이렇게 단순하게 처리하면 라운드 로빈 방식으로 로드 밸런싱 작동.

keepalive 설정을 주는 것이 미세하게 처리 성능에 도움을 준다.(연결을 끊었다가 다시 연결했다가 하는 작업이 없어지기 때문)

upstream myserver 안에 적어주는 서버 리스트들은 원하는 서버들을 적어준다.

아래 server 목록에 적어주는 것은 포트 번호와 기본적인 위치를 지정

이후에 재부팅 후에도 돌아갈 수 있게 systemctl로 등록해준다.

'''
sudo systemctl daemon-reload
sudo systemctl enable nginx
sudo systemctl start nginx
'''

잘 돌아가는지 확인하고 싶을 땐

'''
sudo systemctl status nginx
'''

명령어로 active 상태인지 확인하면 된다.