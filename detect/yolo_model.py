# -*- coding: utf-8 -*-

from functools import reduce
from keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.regularizers import l2


def UpdatedConv2D(*args, **kwargs):
    conv_kwargs = {'kernel_regularizer': l2(5e-4)}
    conv_kwargs['padding'] = 'valid' if kwargs.get('strides') == (2,2) else 'same'
    conv_kwargs.update(kwargs)
    return Conv2D(*args, **conv_kwargs)

def Conv2D_BN_Leaky(*args, **kwargs):
    no_bias_kwargs = {'use_bias': False}
    no_bias_kwargs.update(kwargs)
    return compose_layers(
        UpdatedConv2D(*args, **no_bias_kwargs),
        BatchNormalization(),
        LeakyReLU(alpha=0.1))

def resblock_body(x, num_filters, num_blocks):
    x = ZeroPadding2D(((1,0),(1,0)))(x)
    x = Conv2D_BN_Leaky(num_filters, (3,3), strides=(2,2))(x)
    for i in range(num_blocks):
        y = compose_layers(
                Conv2D_BN_Leaky(num_filters // 2, (1,1)),
                Conv2D_BN_Leaky(num_filters, (3,3)))(x)
        x = Add()([x,y])
    return x

def build_backbone(x):
    x = Conv2D_BN_Leaky(32, (3,3))(x)
    x = resblock_body(x, 64, 1)
    x = resblock_body(x, 128, 2)
    x = resblock_body(x, 256, 8)
    x = resblock_body(x, 512, 8)
    x = resblock_body(x, 1024, 4)
    return x

def build_last_layers(x, num_filters, out_filters):
    x = compose_layers(
            Conv2D_BN_Leaky(num_filters, (1,1)),
            Conv2D_BN_Leaky(num_filters * 2, (3,3)),
            Conv2D_BN_Leaky(num_filters, (1,1)),
            Conv2D_BN_Leaky(num_filters * 2, (3,3)),
            Conv2D_BN_Leaky(num_filters, (1,1)))(x)
    y = compose_layers(
            Conv2D_BN_Leaky(num_filters * 2, (3,3)),
            UpdatedConv2D(out_filters, (1,1)))(x)
    return x, y

def compose_net(inputs, num_anchors, num_classes):
    backbone = Model(inputs, build_backbone(inputs))
    x, y1 = build_last_layers(backbone.output, 512, num_anchors * (num_classes + 5))

    x = compose_layers(
            Conv2D_BN_Leaky(256, (1,1)),
            UpSampling2D(2))(x)
    x = Concatenate()([x,backbone.layers[152].output])
    x, y2 = build_last_layers(x, 256, num_anchors * (num_classes + 5))

    x = compose_layers(
            Conv2D_BN_Leaky(128, (1,1)),
            UpSampling2D(2))(x)
    x = Concatenate()([x,backbone.layers[92].output])
    x, y3 = build_last_layers(x, 128, num_anchors * (num_classes + 5))

    return Model(inputs, [y1, y2, y3])

def compose_layers(*funcs):
    return reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)
