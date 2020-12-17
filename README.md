## 모델 실행 방법

    1. Detecting 모델에서 가중치 생성
    2. 생성된 가중치 파일 'data' 폴더에 넣기
    3. python save_model.py -- weights ./data/'생성한 가중치 파일'.weights --output ./checkpoints/yolov4-416 --input_size 416 --model yolov4
    4. python object_tracker.py --video ./data/video/'test'.mp4 --output ./outputs/'demo'.avi --model yolov4
    *이렇게 하면 분석 영상 파일명 : 'test', 최종 분석 파일명 : 'demo'*
    5. 'count', 'location' 플래그를 사용하여 원하는 기능 추가 가능


### 우리가 생성한 가중치

[다운로드](https://drive.google.com/file/d/1gFMK0r-rlmKSSlaiUJCNvuK5Sy7nYHCL/view?usp=sharing)


## YOLO v4 사용 방법

[바로가기](https://gitlab.com/seoungjun_kim/test1)


## 웹 구동하는 방법

    1. mysql.cnf 파일 생성 - django 프로젝트 최상위 폴더에 생성 (host, database, password, user)
    2. settings.py - AWS setting 계정 정보 수정
    3. view.py - 다른 서버와 통신하는 부분 IP 자신의 환경에 맞게 수정
    4. python manage.py runserver ~.~.~.~:포트번호 입력하여 서버 구동 시작
    
웹 구동에 필요한 자료는 바로 이 깃허브에 다 있습니다.

*중간중간 설치가 되어 있지 않은(무엇무엇이 없다고 나옴) 패키지들은 패키지명이 에러 메시지에 같이 나오니까 패키지들을 설치하시면 됩니다.*


## Ubuntu + Nginx 로 로드밸런싱 구현한 방법

1. 우분투에서 nginx 설치

2. 패키지 설치 완료 후 /etc/nginx/sites-available 디렉토리로 이동

3. sudo vi default 명령어로 파일 생성 후 아래와 같이 작성

```
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
```

[default 파일 깃허브 위치](https://github.com/dldidfh/Traffic-data-generation/blob/master/API_SERVER/linux_load_balancer/default)

이렇게 단순하게 처리하면 라운드 로빈 방식으로 로드 밸런싱 작동.

keepalive 설정을 주는 것이 미세하게 처리 성능에 도움을 준다.(연결을 끊었다가 다시 연결했다가 하는 작업이 없어지기 때문)

upstream myserver 안에 적어주는 서버 리스트들은 원하는 서버들을 적어준다.

아래 server 목록에 적어주는 것은 포트 번호와 기본적인 위치를 지정

이후에 재부팅 후에도 돌아갈 수 있게 systemctl로 등록해준다.

```
sudo systemctl daemon-reload
sudo systemctl enable nginx
sudo systemctl start nginx
```

잘 돌아가는지 확인하고 싶을 땐

```
sudo systemctl status nginx
```

명령어로 active 상태인지 확인하면 된다. 아래 이미지 참조.

<img width="522" alt="2" src="https://user-images.githubusercontent.com/67957934/102457081-84562c00-4085-11eb-99ff-2ee7748b2116.png">


## EC2 새로 만들 때(+ 재시작시) 자동으로 서버 구동하게 설정하는 방법

EC2 생성 시작 템플릿 - 고급 세부 정보 - 사용자 데이터에 아래와 같은 코드를 추가한다.

```
#!/bin/bash
sudo chmod 755 /home/ec2-user/runserver.service
sudo chmod 755 /home/ec2-user/runserver.sh
sudo mv /home/ec2-user/runserver.service /etc/systemd/system/runserver.service
sudo systemctl daemon-reload
sudo systemctl enable runserver
sudo systemctl start runserver
sudo python3.8 /home/ec2-user/Demacia/manage.py runserver 0.0.0.0:8000
```

여기에 필요한 runserver.service 와 runserver.sh 는

[runserver 관련 깃허브 위치](https://github.com/dldidfh/Traffic-data-generation/tree/master/WEB)

이후에 EC2 접속 후 잘 돌아가고 있는지 확인하고 싶을 때는

```
sudo systemctl status runserver
```

명령어를 확인하여 active 상태인지 확인한다.