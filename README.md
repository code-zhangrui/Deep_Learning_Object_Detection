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

#### 1.需要从网上下载预训练权重文件 yolo.h5

#### 2.为模型的改变生成迁移文件
python manage.py makemigrations

#### 3.在数据库里创建新定义的模型的数据表，应用数据库迁移
python manage.py migrate

#### 4.本地启动
python manage.py runserver 7007

#### 5.打开 127.0.0.1:7007/detect
