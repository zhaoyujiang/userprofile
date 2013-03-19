#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import UserProfile, GroupProfile

admin.site.register(UserProfile)
admin.site.register(GroupProfile)
