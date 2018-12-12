# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from subprocess import PIPE, Popen
# Create your views here.
proc = None

def homePageView(request):
    return HttpResponse('Hello, World!')

def start(request):
    global proc
    proc = Popen(['omxplayer', '-o', 'hdmi', '/media/pi/USB-HDD/download/Loving.Pablo.2017.BDRip.x264.HuN-No1/loving.pablo.bdrip-no1.mkv'], stdin=PIPE)
    return HttpResponse(request)

def send_command(request, cmd):
    global proc
    proc.stdin.write(cmd+'\n')
    return HttpResponse(request)

