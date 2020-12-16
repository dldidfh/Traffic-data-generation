# import the module
import pymysql
import os
import pandas as pd
import subprocess
class SaveDataToCSV_DB():
    def __init__(self,line_list, line_classes, video_path, output_path):
        # video_path 형식 : 'upload_origin_video/upload_video/video/test.mkv'
        # output_path 형식 : 'upload_converted_video/upload_video/video/converted_test.mkv'        
        self.line_classes = line_classes
        self.line_list = line_list
        self.video_path = video_path
        self.output_path = output_path
        self.only_file_name = os.path.split(output_path)[1].split('.')[0]
        self.csv_file_path = 'csv/'+self.only_file_name + '.csv'

    def save_to_csv(self):
        # CSV 파일 저장 위치 : '/upload_video/csv/test.csv
        # 변환된 영상 저장 위치 : upload_video/converted_video/test.mkv
        for line_lenght_1 in range(len(self.line_list)):
            self.line_classes.pop(str(line_lenght_1) + '-->' + str(line_lenght_1))
        df = pd.DataFrame(data=self.line_classes)
############################## 경로 설정 해야함##################################
        
        df.to_csv(self.csv_file_path, index=True, header=True)
        
    def save_to_DB(self):
        # csv 파일 위치 저장 
        # csv 파일 저장 위치 : 
        subprocess.check_call('aws s3 cp ' +self.csv_file_path + ' s3://demacia-s3-second/upload_video/csv/', shell=True)
        # 변환 영상 S3 저장
        subprocess.check_call('aws s3 cp ' + self.output_path + " s3://demacia-s3-second/upload_video/converted_video/ --content-type 'application/actet-stream'" , shell=True)

        demacia_db = pymysql.connect(
            host='host', 
            user='user', 
            passwd='password', 
            db='database', 
            port=3306,
            use_unicode = True,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with demacia_db.cursor() as cursor:        
                csv_file = 'upload_video/' + self.csv_file_path
                upload_file = 'upload_video/video/' + os.path.split(self.video_path)[1]
                convert_file = 'upload_video/converted_video/converted_' +  os.path.split(self.video_path)[1]
                sql = """UPDATE DemaciaApp_videofile SET csv_file = '{}' , 
                        state=2, convert_file = '{}' where upload_file = '{}';
                        """.format(csv_file, convert_file, upload_file)
                cursor.execute(sql)
            demacia_db.commit()
        finally:
            demacia_db.close()
