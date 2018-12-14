# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from subprocess import PIPE, Popen
from models import *
from os import walk, path
from django.template import loader
from time import sleep

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
    global proc
    if proc and proc.poll() == None:
        controll_list = []
        controlls = controll.objects.filter(command=proc.cmd)
        for cont in controlls:
            controll_list.append(cont.action)
        context = {
            'controll_list': controll_list
        }
        template = loader.get_template('actions.html')
        return HttpResponse(template.render(context, request))
    global file_list
    create_file_list()
    context = {
        'file_list': file_list
    }
    template = loader.get_template('main.html')
    return HttpResponse(template.render(context, request))

def start(request):
    global proc
    global file_list
    if request.method == 'POST':
        file_num = int(request.POST.get('id'))

        cmd = command.objects.get(media=file_list[file_num][1], active=True)
        options = command_options.objects.filter(command=cmd, active=True)
        popen_list = []
        popen_list.append(str(cmd.command))
        for option in options:
            popen_list.append(str(option.option))
            if option.value:
                popen_list.append(str(option.value))
        popen_list.append(str(file_list[file_num][0]))

        if proc and proc.poll() == None:
            proc.kill()
            proc.cmd = None
        proc = Popen(popen_list, stdin=PIPE, shell=False)
        proc.cmd = cmd
        response = redirect('/server/')
        return response
    return HttpResponse('nok')

def send_action(request):
    global proc
    if request.method == 'POST':
        action = controll.objects.get(command=proc.cmd, action=str(request.POST.get('action')))
        proc.stdin.write(str(action.key))
        response = redirect('/server/')
        sleep(1)
        return response
    return HttpResponse('nok')

