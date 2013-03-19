# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User, Group

def get_group_owner(name):
    try:
        group = Group.objects.get(name=name)
        owner = group.groupprofile.owner
        return owner.username
    except :
        return

def get_dept_group(username):
    try:
        user = User.objects.get(username=username)
        groups = user.groups.all()
        for g in groups:
            if g.name[-5:] == '.DEPT':
                return g.name
    except :
        return

def get_pd_groups(username):
    pd = []
    try:
        user = User.objects.get(username=username)
        groups = user.groups.all()
        for g in groups:
            if g.name[-3:] == '.PD':
                pd.append(g.name)
        return pd
    except :
        return

def get_user_groups(username):
    groups = []
    try:
        user = User.objects.get(username=username)
        gps = user.groups.all()
        for g in gps:
            groups.append(g.name)
        return groups
    except :
        return

def get_user_exist(username):
    exist = False
    try:
        User.objects.get(username=username)
        exist = True
    except :
        pass
    return exist

def get_dept_desc_list():
    dept_desc = []
    try:
        groups = Group.objects.all()
        for g in groups:
            if g.name[-5:] == '.DEPT':
                dept_desc.append((g.name,g.groupprofile.description))
        dept_desc.insert(0, ('',''))#增加一个空白项
        return dept_desc
    except :
        return

def get_groupnumber_exist(groupnumber):
    exist = False
    groups = Group.objects.all()
    for g in groups:
        if g.name[-5:] == '.DEPT' and g.groupprofile.groupnumber == groupnumber:
            exist = True
            return exist
    return exist

def get_deptdesc_number_dict():
    dept_number_dict = {}
    groups = Group.objects.all()
    for g in groups:
        if g.name[-5:] == '.DEPT':
            dept_number_dict[g.groupprofile.description] = g.groupprofile.groupnumber
    return dept_number_dict