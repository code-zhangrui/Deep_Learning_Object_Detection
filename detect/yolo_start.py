# -*- coding: utf-8 -*-

from django.conf import settings
import os
import numpy as np
from PIL import Image, ImageDraw
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from keras.utils import multi_gpu_model
from detect.yolo_model import compose_net
from detect.yolo_param import generate_parameters

os.environ['CUDA_VISIBLE_DEVICES'] = '0'


class YOLO(object):
    def __init__(self):
        self.model_path = settings.DATA_ROOT + '/detect/model_data/yolo.h5'
        self.anchors_path = settings.DATA_ROOT + '/detect/model_data/yolo_anchors.txt'
        self.classes_path = settings.DATA_ROOT + '/detect/model_data/coco_classes.txt'
        self.score = 0.3
        self.iou = 0.45
        self.class_names = self.get_class()
        self.anchors = self.get_anchors()
        self.sess = K.get_session()
        self.model_image_size = (416, 416)
        self.boxes, self.scores, self.classes = self.detect_image()

    def get_class(self):
        classes_path = settings.DATA_ROOT + '/detect/model_data/coco_classes.txt'
        with open(classes_path, 'r', encoding='utf-8') as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def get_anchors(self):
        anchors_path = settings.DATA_ROOT + '/detect/model_data/yolo_anchors.txt'
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def detect_image(self):
        model_path = settings.DATA_ROOT + '/detect/model_data/yolo.h5'
        self.yolo_model = compose_net(Input(shape=(None,None,3)), len(self.anchors)//3, len(self.class_names))
        self.yolo_model.load_weights(self.model_path)
        self.input_image_shape = K.placeholder(shape=(2, ))
        boxes, scores, classes = generate_parameters(self.yolo_model.output, self.anchors,
                len(self.class_names), self.input_image_shape,
                score_threshold=self.score, iou_threshold=self.iou)
        return boxes, scores, classes

    def handle_image(self, image):
        if self.model_image_size != (None, None):
            boxed_image = self.resize_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = self.resize_image(image, new_image_size)
        image_data = np.expand_dims((np.array(boxed_image, dtype='float32')) / 255., 0)
        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        thickness = (image.size[0] + image.size[1]) // 300
        output_dict = {}
        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]
            output_dict[predicted_class] = np.float64(score)
            draw = ImageDraw.Draw(image)
            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline = (100, 255, 100))
            del draw
        return image, output_dict

    def resize_image(self, image, size):
        iw, ih = image.size
        w, h = size
        scale = min(w / iw, h / ih)
        nw = int(iw * scale)
        nh = int(ih * scale)
        image = image.resize((nw,nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
        return new_image

def start(title, suffix):
    img = settings.MEDIA_ROOT + '/cards/' + title + '.' + suffix
    try:
        image = Image.open(img).convert('RGB')
    except:
        print('打开失败')
    else:
        yolo3 = YOLO()
        r_image, output_dict = yolo3.handle_image(image)
        r_image.save(settings.MEDIA_ROOT + '/papers/' + title + '.' + suffix)
    K.clear_session()
    yolo3.sess.close()
    return output_dict