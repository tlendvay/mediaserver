# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class command(models.Model):
    media = models.CharField(max_length=50, unique=True, verbose_name="Media type")
    command = models.CharField(max_length=50, verbose_name="Command")
    active = models.BooleanField(blank=True, default=True)

    def __str__(self):
        return "{}".format(self.media)


class command_options(models.Model):
    command = models.ForeignKey(command, null=True)
    option = models.CharField(max_length=50, null=True, blank=True, verbose_name="Option")
    value = models.CharField(max_length=50, null=True, blank=True, verbose_name="Value")
    active = models.BooleanField(blank=True, default=True)

class file_extension(models.Model):
    extension = models.CharField(max_length=50, unique=True, verbose_name="Extension")
    media = models.ForeignKey(command, null=True)

class media_path(models.Model):
    directory = models.CharField(max_length=250, unique=True, verbose_name="Path")