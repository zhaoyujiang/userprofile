#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import ldap

from django.conf import settings

from django_auth_ldap.config import LDAPSearch, _DeepStringCoder

def get_ldap_con():
    dn = settings.AUTH_LDAP_BIND_DN
    pw = settings.AUTH_LDAP_BIND_PASSWORD
    con = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
    con.simple_bind_s( dn, pw )
    return con

def simple_ldap_obj(ldap_obj):
    """返回简化过的LDAP对象。LDAP的值都为LIST，经过简化后只保留LIST中的第一个值"""
    new_obj = {}
    for k, v in ldap_obj.items():
        #FIXME LDAP不区分大小写，这个字段库中的大小写和form中的不一致
        if k == 'IdCardNo':
            k = 'idCardNo'
        new_obj[k] = v[0]
    return new_obj

def get_form_val(form, field):
    """获取form的val，主要完成unicode2utf8的转换"""
    return form.cleaned_data[field].encode('utf-8')

def make_mod_attrs(form, skip_fields=['cn']):
    """生成表单的LDAP修改列表"""
    mod_attrs = []
    for k, v in form.cleaned_data.items():
        if not skip_fields.count(k):
            v = None if v == '' else v.encode('utf-8')
            mod_attrs.append((ldap.MOD_REPLACE, k, v))
    return mod_attrs

def make_add_attrs(form, skip_fields=[]):
    """生成表单的LDAP创建属性列表"""
    mod_attrs = []
    for k, v in form.cleaned_data.items():
        if not skip_fields.count(k) and v != '':
            mod_attrs.append(
                    (k, (v.encode('utf-8'),))
                    )
    return mod_attrs

class LDAPSearchExt(LDAPSearch):
    def __init__(self, base_dn, scope, filterstr=u'(objectClass=*)'):
        super(LDAPSearchExt, self).__init__(base_dn, scope, filterstr)

    def execute(self, connection, filterargs=(), attrs=[]):
        try:
            filterstr = self.filterstr % filterargs
            results = connection.search_s(self.base_dn.encode('utf-8'),
                self.scope, filterstr.encode('utf-8'), attrs)
            results = filter(lambda r: r[0] is not None, results)
            results = _DeepStringCoder('utf-8').decode(results)
        except self.ldap.LDAPError, e:
            results = []
        return results
