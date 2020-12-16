import os
import re
# comment out below line to enable tensorflow logging outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    tf.config.experimental.set_memory_growth(physical_devices[1], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from core.config import cfg
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
# counting functions imports
from core.functions import *
# deep sort imports
from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
import pandas as pd
from save_data_to_csv_DB import SaveDataToCSV_DB

import line_draw_mouse_gesture

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('video', './data/video/test.mp4', 'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')  # MP4V  AVC1  XVID
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
flags.DEFINE_boolean('dont_show', False, 'dont show video output')
flags.DEFINE_boolean('info', True, 'show detailed info of tracked objects')
flags.DEFINE_boolean('count', False, 'count objects being tracked on screen')
flags.DEFINE_string('location',None,'location to input video')
flags.DEFINE_string('user_upload',None,'사용자 요청이면 DB에서 저장된 선을 그은 정보를 가져와서 분석을 시작한다')

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def main(_argv):
    # Definition of the parameters
    max_cosine_distance = 0.4
    nn_budget = None
    nms_max_overlap = 1.0
    
    # initialize deep sort
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    # calculate cosine distance metric
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    # initialize tracker
    tracker = Tracker(metric)

    # load configuration for object detector
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    video_path = FLAGS.video
    video_location = FLAGS.location
    db_user_line_list = FLAGS.user_upload
    # print(video_location,'\t모델 분석 시작')
    # load tflite model if flag is set
    if FLAGS.framework == 'tflite':
        interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        # print(input_details)
        # print(output_details)
    # otherwise load standard tensorflow saved model
    else:
        saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default']

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)

    out = None

    # get video ready to save locally if flag is set
    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))
    car = 0
    motor = 0
    bus = 0
    truck = 0
    frame_num = 0
    line_data = []
    memory = {}
   
    
    line_list = [] # 그어진 라인의 위치정보를 담기위한 변수 
    count_result = {} # 라인별로 카운팅 하기위한 변수
    line_classes = {}
    # while video is running
    while True:
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
        else:

            print('Video has ended or failed, try a different video format!')
            break
        frame_num +=1
        if frame_num == 1:             
            # 플레그 location 이 있으면 경로 가져와서 실행 
            # print('비디오 로케이션 위치 : ',video_location)
            # if video_location == None:
            #     line_list = line_draw_mouse_gesture.draw_line(frame)
            if db_user_line_list != None:                
                # print('변환 전',db_user_line_list)
                db_user_line_list = re.findall('\d+',db_user_line_list)
                for i in range(0, len(db_user_line_list)): 
                    db_user_line_list[i] = int(db_user_line_list[i])
                # print('후후후후',db_user_line_list)

                for line_enum in range(int(len(db_user_line_list) / 4)):
                    temp = line_enum * 4
                    line_list.append([(db_user_line_list[temp ],db_user_line_list[temp+1]),(db_user_line_list[temp+2],db_user_line_list[temp+3])])

            elif db_user_line_list == None and video_location == None:
                line_list = line_draw_mouse_gesture.draw_line(frame)
            elif video_location == 'Gongdeok_5_way':
                line_list = [[(324,430), (1019,591)], [(395,200), (242,398)], [(648,137), (986,193)], [(1092,207), (1278,330)], [(1275,353),(1043,588)]]
            elif video_location == 'Seoul_Plaza':
                line_list = [[(415,151) , (329,326)], [(722,218), (736,345)], [(291,419), (659,441)]]
            # elif db_user_line_list != None:                
            #     db_user_line_list = re.findall('\d+',db_user_line_list)
            #     for line_enum in range(int(len(db_user_line_list) / 4)):
            #         line_list.append([(test[line_enum],test[line_enum+1]),(test[line_enum+2],test[line_enum+3])])
                    



            # print('리턴된 값은 ',line_list)    
            for line_list_first in range(len(line_list)):
                for line_list_second in range(len(line_list)):
                    line_classes[str(line_list_first) + '-->' + str(line_list_second)] = {'car' : 0, 'bus' : 0, 'truck' : 0}
            # print('만들어진 라인의 클래스들은 : ',line_classes)
            
            # 동영상 프레임 킨다음 사용자 입력 받게 하고 값 라인에 저장
            # line1 = [(입력값, 입력값), (입력값, 입력값)]
            # line2 = [(입력값, 입력값), (입력값, 입력값)]
        # print('Frame #: ', frame_num)
        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()

        # run detections on tflite if flag is set
        if FLAGS.framework == 'tflite':
            interpreter.set_tensor(input_details[0]['index'], image_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            # run detections using yolov3 if flag is set
            if FLAGS.model == 'yolov3' and FLAGS.tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
        else:
            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )
        # convert data to numpy arrays and slice out unused elements
        num_objects = valid_detections.numpy()[0]
        bboxes = boxes.numpy()[0]
        bboxes = bboxes[0:int(num_objects)]
        scores = scores.numpy()[0]
        scores = scores[0:int(num_objects)]
        classes = classes.numpy()[0]
        classes = classes[0:int(num_objects)]

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, width, height
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(bboxes, original_h, original_w)

        # store all predictions in one parameter for simplicity when calling functions
        pred_bbox = [bboxes, scores, classes, num_objects]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        allowed_classes = list(class_names.values())
        
        # custom allowed classes (uncomment line below to customize tracker for only people)
        # allowed_classes = ['###'] # we can search all information in this cctv

        # loop through objects and use class index to get class name, allow only classes in allowed_classes list
        names = []
        deleted_indx = []

        for i in range(num_objects):
            class_indx = int(classes[i])
            class_name = class_names[class_indx]
            if class_name not in allowed_classes:
                deleted_indx.append(i)
            else:
                names.append(class_name)

        names = np.array(names)
        count = len(names)

        if FLAGS.count:         
            cv2.putText(frame, "Number of Objects being tracked: {}".format(count), (5, 35), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 2)
            print("Number of Objects being tracked: {}".format(count))

            # count objects found
            counted_classes = count_objects(pred_bbox, by_class = True, allowed_classes = allowed_classes)

            # loop through dict and print
            # for key, value in counted_classes.items():
            #     pass
                # print("Number of {}: {}".format(key, value))

        # delete detections that are not in allowed_classes
        bboxes = np.delete(bboxes, deleted_indx, axis=0)
        scores = np.delete(scores, deleted_indx, axis=0)

        # encode yolo detections and feed to tracker
        features = encoder(frame, bboxes)
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(bboxes, scores, names, features)]

        #initialize color map
        cmap = plt.get_cmap('tab20b')
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

        # run non-maxima supression
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(boxs, classes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]       

        # Call the tracker
        tracker.predict()
        tracker.update(detections)
#####################양로의 코딩#########################################               
        
        trigger = 0
        # update tracks
        track_len = len(tracker.tracks)
        # frame_num 에는 프레임 수가 담겨있다
        # track 에는 하나의 객체검출 정보가 담겨있다 
        # print('객체정보의 길이는 ',len(tracker.tracks))
        i = int(0)
        
        previous = memory.copy()
        memory = {}
        boxes = []
        indexIDs = []
        for track in tracker.tracks:
            
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()
            class_name = track.get_class()
            boxes.append([bbox[0], bbox[1], bbox[2], bbox[3], class_name])
            indexIDs.append(int(track.track_id))
            memory[indexIDs[-1]] = boxes[-1]
        
#####################양로의 코딩#########################################                   
            
            # draw bbox on screen
            color = colors[int(track.track_id) % len(colors)]
            color = [i * 255 for i in color]
#####################양로의 코딩#########################################    

            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 1)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1]-20)), (int(bbox[0])+(len(class_name)+len(str(track.track_id)))*10, int(bbox[1])), color, -1)
            cv2.putText(frame, class_name + "-" + str(track.track_id),(int(bbox[0]), int(bbox[1]-2)),0, 0.4, (255,255,255),2)
            for i in range(len(line_list)):
                line_number_position = (line_list[i][0][0] , int(line_list[i][0][1]) - 20 )
                cv2.putText(frame, 'Line Number ' + str(i),line_number_position,0, 0.5,(255,0,0),2)
                cv2.line(frame,(line_list[i][0]), (line_list[i][1]), (255,0,0), 2)

        if len(boxes) > 0:
            i = int(0)
            
            for box in boxes:
                # extract the bounding box coordinates
                (x, y) = (int(box[0]), int(box[1]))
                (w, h) = (int(box[2]), int(box[3]))
                

                if indexIDs[i] in previous:
                    previous_box = previous[indexIDs[i]]
                    (x2, y2) = (int(previous_box[0]), int(previous_box[1]))
                    (w2, h2) = (int(previous_box[2]), int(previous_box[3]))
                    p0 = (int(x + (w-x)/2), int(y + (h-y)/2))
                    p1 = (int(x2 + (w2-x2)/2), int(y2 + (h2-y2)/2))

                    for k in range(len(line_list)):
                        # 라인 넘버는 k 
                        if indexIDs[i] not in count_result:
                            count_result[indexIDs[i]] = []

                        if intersect(p0, p1, line_list[k][0],line_list[k][1]):
                            detected_class = box[4]
                            count_result[indexIDs[i]].append(k)
                            # print('카운트 리저트 값 : ',count_result)
                            if len(count_result[indexIDs[i]]) == 2:
                                # print('인덱스 아이번째 값은 ',count_result[indexIDs[i]])
                                # print('인덱스 아이번째 값은 ',count_result[indexIDs[i]][0])
                                linenum1 = count_result[indexIDs[i]][0]
                                linenum2 = count_result[indexIDs[i]][1]
                                # print('라인 넘버 몇일까',linenum1,linenum2)

                                # 카운트를 증가시키고 
                                # 그 아이디벨류를 삭제 시키고 
                            
                                if detected_class == 'car':
                                    line_classes[str(linenum1) + '-->' + str(linenum2)]['car'] +=1
                                    # count_result[indexIDs][] +=1
                                    # car = car + 1
                                elif detected_class == 'truck':
                                    line_classes[str(linenum1) + '-->' + str(linenum2)]['truck'] +=1
                                    # count_result[str(k+1)+'truck'] +=1
                                    # truck = truck + 1
                                elif detected_class == 'bus':
                                    line_classes[str(linenum1) + '-->' + str(linenum2)]['bus'] +=1
                                    # count_result[str(k+1)+'bus'] +=1
                                    # bus = bus+1
                                else:
                                    print('예외치 검출')
                                # print(count_result)
                                count_result.pop(indexIDs[i])
                                # print('카운트 결과값 제거 후에 어떻게 됬나',count_result)
                    '''        
                    if p0[0] > 921 and p0[0] < 1440 and p0[1] < 606 and p0[1] > 437:
                        p0Memory = p0
                        state = True
                        if 
                    '''        

                i += 1
        
        # if enable info flag then print details about each track
            if FLAGS.info:
                pass
        for line_lenght_1 in range(len(line_list)):
            for line_lenght_2 in range(len(line_list)):
                text_text = '{} --> {} = Car : {} Bus : {} Truck : {}'.format(
                    line_lenght_1, 
                    line_lenght_2,
                    line_classes[str(line_lenght_1) + '-->'+str(line_lenght_2)]['car'],
                    line_classes[str(line_lenght_1) + '-->'+str(line_lenght_2)]['bus'],
                    line_classes[str(line_lenght_1) + '-->'+str(line_lenght_2)]['truck'])
                cv2.putText(frame, text_text, (line_list[line_lenght_1][0][0],int(line_list[line_lenght_1][0][1])+ line_lenght_2*15)  , 0,0.5, (0,255,0), 2)        

        # print(tracker._next_id)

        # calculate frames per second of running detections
        fps = 1.0 / (time.time() - start_time)
        # print("FRAME : {} \t FPS: {}".format(frame_num, fps))
        result = np.asarray(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if not FLAGS.dont_show:
            cv2.imshow("Output Video", result)
        
        # if output flag is set, save video file
        if FLAGS.output:
            out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    # line_list : 사용자가 입력한 라인 정보
    # line_classes : 총 통계된 결과
    # video_path : 입력된 비디오 파일 경로 

    
        
        # csv파일 생성 
        
        # S3 csv, DB 저장
        

        
    cv2.destroyAllWindows()
    if db_user_line_list != None:
        result = SaveDataToCSV_DB(line_list, line_classes, video_path, FLAGS.output)
        result.save_to_csv()
        result.save_to_DB()
        # result.delete_converted_files()


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
