## 모델 실행 방법

    1. Detecting 모델에서 가중치 생성
    2. 생성된 가중치 파일 'data' 폴더에 넣기
    3. python save_model.py -- weights ./data/'생성한 가중치 파일'.weights --output ./checkpoints/yolov4-416 --input_size 416 --model yolov4
    4. python object_tracker.py --video ./data/video/'test'.mp4 --output ./outputs/'demo'.avi --model yolov4
    *이렇게 하면 분석 영상 파일명 : 'test', 최종 분석 파일명 : 'demo'*
    5. 'count', 'location' 플래그를 사용하여 원하는 기능 추가 가능

## YOLO v4 사용 방법

[바로가기](https://gitlab.com/seoungjun_kim/test1)

