from operator import mod
import os
import sys
from pathlib import Path
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import shutil
from django.conf import settings
from django.db import models
from django.dispatch import receiver

class Board(models.Model):
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=10, null=False)
    content = models.TextField(null=False)
    password = models.CharField(max_length=20, null=False, default='1234')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    files = models.FileField(upload_to="",null=True)
    detect_files = models.FileField(upload_to="detect/",null=True)
    status = models.IntegerField(default=0,null=False)
    detact_result = models.CharField(max_length=50, default="0.0",null=False)

    def __str__(self):
        return str(self.title)

@receiver(models.signals.pre_save, sender=Board)
def auto_delete_file_on_save(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False
    
    for field in instance._meta.fields:
        field_type = field.get_internal_type()
        if field_type == 'FileField' or field_type == 'ImageField':
            origin_file = getattr(old_obj, field.name)
            new_file = getattr(instance, field.name)
            print(origin_file, new_file)
            if origin_file != new_file and os.path.isfile(origin_file.path):
                os.remove(origin_file.path)

@receiver(models.signals.post_delete, sender=Board)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    for field in instance._meta.fields:
        field_type = field.get_internal_type()
        if field_type == 'FileField' or field_type == 'ImageField':
            origin_file = getattr(instance, field.name)
            if origin_file and os.path.isfile(origin_file.path):
                os.remove(origin_file.path)

@receiver(models.signals.post_save, sender=Board)
def detect(sender, instance, **kwargs):
    for field in instance._meta.fields:
        field_type = field.get_internal_type()
        if field_type == 'FileField' or field_type == 'ImageField':
            videocheck = getattr(instance, field.name)
            print(str(videocheck))
            FILE = Path(__file__).resolve()
            ROOT2 = FILE.parents[1]
            MASK_ROOT = os.path.join(ROOT2, "Mask_RCNN" , "video_detect.py")
            video_detect = "python " + MASK_ROOT + " " + str(videocheck)

            #감지 쓰레드 실행
            th1 = threading.Thread(target=excute_detect, args=(video_detect,))
            th1.start()
            #파일 생성 쓰레드 실행
            status_watch = S_Target()
            th2 = threading.Thread(target=modify_status, args=(status_watch,th1,instance.id,str(videocheck),))
            th2.start()

            print("영상 업로드 완료")


def modify_status(status_watch, thread, db_id, video):
    result_status = status_watch.run()
    thread.join() #이건 쓰레드 한번 더 실행되는 문제 발생
    status_txt = open(os.path.join(result_status, "status.txt"))
    status_result = status_txt.readlines()
    detected_file = os.path.join(result_status, video)



    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]
    media_root = os.path.join(ROOT, "media", "detect")
    detected_file_root = os.path.join(media_root, video)

    interface_root = os.path.join(ROOT, "cctv_interface", "public", "videos")
    detected_interface = os.path.join(interface_root, video)

    print("검출경로 : " + detected_file_root)
    if not os.path.exists(media_root):
        os.makedirs(media_root)
        shutil.copy2(detected_file, detected_file_root)
        print("디렉토리 및 파일 이동 성공")
    else:
        shutil.copy2(detected_file, detected_file_root)
        print("파일 이동 성공")

    warn_cnt = re.findall("\d+", status_result[0])
    danger_cnt = re.findall("\d+", status_result[1])
    result_percent = re.findall("\d+\.\d+", status_result[2])

    post_list = Board.objects.filter(id=db_id)
    #
    if int(danger_cnt[0]) > 24:
        post_list.update(status=3, detect_files="detect/" + video, detact_result=100.0)
    elif int(warn_cnt[0]) > 24:
        post_list.update(status=2, detect_files="detect/" + video, detact_result=str(result_percent)[2:12])
    else:
        post_list.update(status=1, detect_files="detect/" + video)



def excute_detect(os_str):
    os.system(os_str)




class S_Target:
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]
    watchDir = os.path.join(ROOT, "yolov5", "runs", "detect")
    #watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir,
                                                       recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
                if event_handler.observer_success:
                    self.observer.stop()
                    return event_handler.result_path

        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함
    observer_success = False
    result_path = None
    #파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        print(event)

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        print(event)
        print("생성된 디렉토리 : " + event.src_path)
        self.observer_success = True
        self.result_path = event.src_path

    def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
        print(event)

    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        print(event)
