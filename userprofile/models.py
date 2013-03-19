# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

# Create your models here.

BOOLEAN_CHOICES = (
    ('', u'...'),
    ('Y', u'是'),
    ('N', u'否'),
)
GENDER_CHOICES = (
    ('', u'...'),
    ('M', u'男'),
    ('F', u'女'),
)
EMPLOYEE_TYPE_CHOICES = (
    ('P', u'正式员工'),
    ('S', u'实习'),
)
EMPLOYEE_STATUS_CHOICES = (
    ('A', u'激活'),
    ('D', u'离职'),
    ('H', u'非激活'),#休眠账号
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    cnName = models.CharField(max_length=50, blank=True, null=True)
    displayName = models.CharField(max_length=50, blank=True, null=True)
    privateMail = models.EmailField(blank=True, null=True)
    qq = models.CharField(max_length=50, blank=True, null=True)
    msn = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    telephoneNumber = models.CharField(max_length=40, blank=True, null=True)
    employeeType = models.CharField(choices=EMPLOYEE_TYPE_CHOICES, blank=True, max_length=10, null=True)
    homePostalAddress = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=10, null=True)
    birthday = models.CharField(max_length=50, blank=True, null=True)
    married = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, blank=True)
    idCardNo = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(choices=EMPLOYEE_STATUS_CHOICES, max_length=10)
    description = models.CharField(max_length=100, blank=True, null=True)
    technologyLevel = models.CharField(max_length=20, blank=True, null=True)
    employeeNumber = models.CharField(max_length=50, blank=True, null=True)
    workingTime = models.DateField(blank=True, null=True)
    entryTime = models.DateField(blank=True, null=True)
    regularTime = models.DateField(blank=True, null=True)
    is_regular = models.BooleanField(default=True)
    pswd_update_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    inactive_datetime = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.get_cnname()

    def get_cnname(self):
        """如果没有中文名字，返回用户名"""
        return self.cnName if self.cnName else self.user.username

class GroupProfile(models.Model):
    group = models.OneToOneField(Group)

    groupnumber = models.CharField(max_length=30, blank=True, null=True)
    owner = models.ForeignKey(User, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.group

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def creat_group_profile(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.create(group=instance)

post_save.connect(create_user_profile, sender=User)
post_save.connect(creat_group_profile, sender=Group)

