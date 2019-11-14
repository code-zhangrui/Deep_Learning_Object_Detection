# Deep_Learning_Object_Detection_Project
Object Detection

===========================

## 环境依赖
python==3.6.4

Django==2.0.6

gunicorn==19.8.1

Keras==2.1.5

Pillow==5.0.0

protobuf==3.6.0

tensorflow==1.5.0

matplotlib==2.2.2

h5py==2.8.0rc1

## 本地部署

- 下载预训练权重文件 yolo.h5
- https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5

- python manage.py makemigrations

- python manage.py migrate

- python manage.py runserver 7007

- 127.0.0.1:7007/detect
