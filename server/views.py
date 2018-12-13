# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from subprocess import PIPE, Popen
from models import *
from os import walk, path
from django.template import loader

# Create your views here.
proc = None
file_list = []

def create_file_list():
    global file_list
    file_list = []
    extensions = {}
    for extension in file_extension.objects.all():
        extensions[extension.extension] = extension.media
    for media_dir in media_path.objects.all():
        for dirpath, dirnames, filenames in walk(media_dir.directory):
            for file in filenames:
                if file.split('.')[-1] in extensions.keys():
                    file_list.append((path.join(dirpath, file), extensions[file.split('.')[-1]]))




def homePageView(request):
    global file_list
    create_file_list()
    context = {
        'file_list': file_list
    }
    template = loader.get_template('main.html')
    return HttpResponse(template.render(context, request))

def start(request, num):
    global proc
    global file_list
    file_num = int(num)
    if file_num < len(file_list):

        cmd = command.objects.get(media=file_list[file_num][1], active=True)
        options = command_options.objects.filter(command=cmd, active=True)
        popen_list = []
        popen_list.append(str(cmd.command))
        for option in options:
            popen_list.append(str(option.option))
            popen_list.append(str(option.value))
        popen_list.append(str(file_list[file_num][0]))

        if proc and proc.poll() == None:
            proc.kill()
        #proc = Popen("cmd", stdin=PIPE)
        proc = Popen(popen_list, stdin=PIPE)
        return HttpResponse(popen_list)
    return HttpResponse('nok')

def send_command(request, cmd):
    global proc
    proc.stdin.write(cmd+'\n')
    return HttpResponse(request)

