import sys
sys.path.append("..")
import vnn
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

#FC model

def make_mnist_vec_fc(mono=False):
    model = nn.Sequential(
        vnn.Linear(10, 28*28*10, 1024, first_layer=True, mono=mono),
        vnn.tReLU(10, 1024),
        vnn.Linear(10, 1024, 512, mono=mono),
        vnn.tReLU(10, 512),
        vnn.Linear(10, 512, 1, mono=mono))
    return model

def make_mnist_nonvec_fc():
    model = nn.Sequential(
        nn.Linear(28*28, 1024),
        nn.ReLU(),
        nn.Linear(1024, 512),
        nn.ReLU(),
        nn.Linear(512, 10))
    return model

def make_cifar_vec_fc(mono=False):
    model = nn.Sequential(
        vnn.Linear(10, 32*32*3*10, 1024, first_layer=True, mono=mono),
        vnn.tReLU(10, 1024),
        vnn.Linear(10, 1024, 512, mono=mono),
        vnn.tReLU(10, 512),
        vnn.Linear(10, 512, 512, mono=mono),
        vnn.tReLU(10, 512),
        vnn.Linear(10, 512, 512, mono=mono),
        vnn.tReLU(10, 512),
        vnn.Linear(10, 512, 1, mono=mono))
    return model

def make_cifar_nonvec_fc():
    model = nn.Sequential(
        nn.Linear(32*32*3, 1024),
        nn.ReLU(),
        nn.Linear(1024, 512),
        nn.ReLU(),
        nn.Linear(512, 512),
        nn.ReLU(),
        nn.Linear(512, 512),
        nn.ReLU(),
        nn.Linear(512, 10))
    return model

#Conv model

def make_mnist_vec_conv(mono=False):
    model = nn.Sequential(
        vnn.Conv2d(10, 10, 128, 3, stride=1, padding=1, first_layer=True, mono=mono),
        vnn.ctReLU(10, 128, 28, 28),
        vnn.AvgPool2d(2),
        vnn.Conv2d(10, 128, 128, 3, stride=1, padding=1, mono=mono),
        vnn.ctReLU(10, 128, 14, 14),
        vnn.AvgPool2d(2), #7 by 7
        vnn.Flatten(),
        vnn.Linear(10, 6272, 1024, mono=mono),
        vnn.tReLU(10, 1024),
        vnn.Linear(10, 1024, 1, mono=mono))
    return model

def make_mnist_nonvec_conv():
    model = nn.Sequential(
        nn.Conv2d(1, 128, 3, stride=1, padding=1),
        nn.ReLU(),
        nn.AvgPool2d(2),
        nn.Conv2d(128, 128, 3, stride=1, padding=1),
        nn.ReLU(),
        nn.AvgPool2d(2), #7 by 7
        nn.Flatten(),
        nn.Linear(6272, 1024),
        nn.ReLU(),
        nn.Linear(1024, 10))
    return model

def make_cifar_vec_conv(mono=False):
    model = nn.Sequential(
        vnn.Conv2d(10, 30, 256, 5, stride=1, padding=2, first_layer=True, mono=mono),
        vnn.ctReLU(10, 256, 32, 32),
        vnn.AvgPool2d(2),
        vnn.Conv2d(10, 256, 256, 5, stride=1, padding=2, mono=mono),
        vnn.ctReLU(10, 256, 16, 16),
        vnn.AvgPool2d(2),
        vnn.Conv2d(10, 256, 256, 2, stride=2, padding=0, mono=mono),
        vnn.ctReLU(10, 256, 4, 4),
        vnn.Flatten(),
        vnn.Linear(10, 4096, 1024, mono=mono),
        vnn.tReLU(10, 1024),
        vnn.Linear(10, 1024, 1, mono=mono))
    return model

def make_cifar_nonvec_conv(mono=False):
    model = nn.Sequential(
        nn.Conv2d(3, 256, 5, stride=1, padding=2),
        nn.ReLU(),
        nn.AvgPool2d(2),
        nn.Conv2d(256, 256, 5, stride=1, padding=2),
        nn.ReLU(),
        nn.AvgPool2d(2),
        nn.Conv2d(256, 256, 2, stride=2, padding=0),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(4096, 1024),
        nn.ReLU(),
        nn.Linear(1024, 10))
    return model

#LC model

def make_mnist_vec_lc(mono=False):
    model = nn.Sequential(
        vnn.VecLocal2d(10, 10, 128, 3, h_in=28, w_in=28, stride=1, padding=1, first_layer=True, mono=mono),
        vnn.ctReLU(10, 128, 28, 28),
        vnn.AvgPool2d(2),
        vnn.VecLocal2d(10, 128, 128, 3, h_in=14, w_in=14, stride=1, padding=1, mono=mono),
        vnn.ctReLU(10, 128, 14, 14),
        vnn.AvgPool2d(2), #7 by 7
        vnn.Flatten(),
        vnn.Linear(10, 6272, 1024, mono=mono),
        vnn.tReLU(10, 1024),
        vnn.Linear(10, 1024, 1, mono=mono))
    return model

def make_mnist_nonvec_lc():
    model = nn.Sequential(
        vnn.Local2d(1, 128, 3, h_in=28, w_in=28, stride=1, padding=1),
        nn.ReLU(),
        nn.AvgPool2d(2),
        vnn.Local2d(128, 128, 3, h_in=14, w_in=14, stride=1, padding=1),
        nn.ReLU(),
        nn.AvgPool2d(2), #7 by 7
        nn.Flatten(),
        nn.Linear(6272, 1024),
        nn.ReLU(),
        nn.Linear(1024, 10))
    return model

def make_cifar_vec_lc(mono=False):
    model = nn.Sequential(
        vnn.VecLocal2d(10, 30, 128, 5, h_in=32, w_in=32, stride=1, padding=2, first_layer=True, mono=mono),
        vnn.ctReLU(10, 128, 32, 32),
        vnn.AvgPool2d(2),
        vnn.VecLocal2d(10, 128, 128, 5, h_in=16, w_in=16, stride=1, padding=2, mono=mono),
        vnn.ctReLU(10, 128, 16, 16),
        vnn.AvgPool2d(2),
        vnn.VecLocal2d(10, 128, 128, 2, h_in=8, w_in=8, stride=2, padding=0, mono=mono),
        vnn.ctReLU(10, 128, 4, 4),
        vnn.Flatten(),
        vnn.Linear(10, 2048, 1024, mono=mono),
        vnn.tReLU(10, 1024),
        vnn.Linear(10, 1024, 1, mono=mono))
    return model

def make_cifar_nonvec_lc():
    model = nn.Sequential(
        vnn.Local2d(3, 128, 5, h_in=32, w_in=32, stride=1, padding=2),
        nn.ReLU(),
        nn.AvgPool2d(2),
        vnn.Local2d(10, 128, 128, 5, h_in=16, w_in=16, stride=1, padding=2),
        nn.ReLU(),
        nn.AvgPool2d(2),
        vnn.Local2d(128, 128, 2, h_in=8, w_in=8, stride=2, padding=0),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(2048, 1024),
        nn.ReLU(),
        nn.Linear(1024, 10))
    return model




