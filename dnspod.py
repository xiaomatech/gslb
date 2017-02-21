#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
try:
    import simplejson as json
except Exception, e:
    import json

INFO_VERSION_URL = "https://dnsapi.cn/Info.Version"

DOMAIN_LIST_URL = 'https://dnsapi.cn/Domain.List'
DOMAIN_CREATE_URL = 'https://dnsapi.cn/Domain.Create'
DOMAIN_REMOVE_URL = 'https://dnsapi.cn/Domain.Remove'
DOMAIN_STATUS_URL = 'https://dnsapi.cn/Domain.Status'
DOMAIN_INFO_URL = 'https://dnsapi.cn/Domain.Info'
DOMAIN_LOG_URL = 'https://dnsapi.cn/Domain.Log'

DOMAIN_GROUP_LIST_URL = 'https://dnsapi.cn/Domaingroup.List'
DOMAIN_GROUP_CREATE_URL = 'https://dnsapi.cn/Domaingroup.Create'
DOMAIN_GROUP_MODIFY_URL = 'https://dnsapi.cn/Domaingroup.Modify'
DOMAIN_GROUP_REMOVE_URL = 'https://dnsapi.cn/Domaingroup.Remove'
DOMAIN_GROUP_CHANGE_URL = 'https://dnsapi.cn/Domain.Changegroup'

RECORD_LIST_URL = 'https://dnsapi.cn/Record.List'
RECORD_MODIFY_URL = 'https://dnsapi.cn/Record.Modify'
RECORD_CREATE_URL = 'https://dnsapi.cn/Record.Create'
RECORD_REMOVE_URL = 'https://dnsapi.cn/Record.Remove'
RECORD_STATUS_URL = 'https://dnsapi.cn/Record.Status'
RECORD_DDNS_URL  = 'https://dnsapi.cn/Record.Ddns'
RECORD_REMARK_URL = 'https://dnsapi.cn/Record.Remark'
RECORD_INFO_URL = 'https://dnsapi.cn/Record.Info'

USER_DETAIL_URL = 'https://dnsapi.cn/User.Detail'

RECORD_TYPES = ["A", "CNAME", "MX", "URL", "NS", "TXT", "AAAA", "SRV"]

RECORD_LINES = ["默认","国内","国外","电信","联通","教育网","移动","百度","谷歌","搜搜","有道","必应","搜狗","奇虎","搜索引擎"]

class Dnspod():
    def __init__ (self, login_token):
        
        self.headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' }
        self.values = {'login_token' : login_token,
                       'lang':'cn',
                       'format' : 'json' }

    def request(self,url,req_data):
        data = urllib.urlencode(req_data)
        info_version_req = urllib2.Request(url, data, self.headers)
        response = urllib2.urlopen(info_version_req)
        ret = response.read()
        return json.loads(ret)

    def get_user_detail(self):
        return self.request(USER_DETAIL_URL,self.values)

    def get_info_version (self):
        return self.request(INFO_VERSION_URL,self.values)

    def get_record_list(self, domain_id):
        req_data = self.values.copy()
        req_data['length'] = '30'
        req_data['offset'] = '0'
        req_data['domain_id'] = domain_id
        return self.request(RECORD_LIST_URL,req_data)

    def modify_record(self, domain_id, record_id, sub_domain, record_type, \
                     record_line, record_value, record_mx=10, record_ttl=86400):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['record_id'] = record_id
        req_data['sub_domain'] = sub_domain
        req_data['record_type'] = record_type
        req_data['record_line'] = record_line
        req_data['value'] = record_value
        req_data['mx'] = record_mx
        req_data['ttl'] = record_ttl
        return self.request(RECORD_MODIFY_URL,req_data)

    def remove_record(self, domain_id, record_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['record_id'] = record_id
        return self.request(RECORD_REMOVE_URL,req_data)

    def create_rcord(self, domain_id, sub_domain, record_type, record_line, \
                    record_value, record_mx=20, record_ttl=86400):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['sub_domain'] = sub_domain
        req_data['record_type'] = record_type
        req_data['record_line'] = record_line
        req_data['value'] = record_value
        req_data['mx'] = record_mx
        req_data['ttl'] = record_ttl
        return self.request(RECORD_CREATE_URL,req_data)

    def modify_record_ddns(self, domain_id, record_id, sub_domain, record_type, \
                      record_line, record_value):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['record_id'] = record_id
        req_data['sub_domain'] = sub_domain
        req_data['record_type'] = record_type
        req_data['record_line'] = record_line
        req_data['value'] = record_value
        return self.request(RECORD_DDNS_URL,req_data)

    def remark_record(self,domain_id,record_id,remark):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['record_id'] = record_id
        req_data['remark'] = remark
        return self.request(RECORD_REMARK_URL,req_data)

    def info_record(self,domain_id,record_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['record_id'] = record_id
        return self.request(RECORD_INFO_URL,req_data)

    def enable_record(self,domain_id,record_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['record_id'] = record_id
        req_data['status'] = 'enable'
        return self.request(RECORD_STATUS_URL,req_data)

    def disable_record(self,domain_id,record_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['record_id'] = record_id
        req_data['status'] = 'disable'
        return self.request(RECORD_STATUS_URL,req_data)

    def create_domain(self, domain):
        req_data = self.values.copy()
        req_data['domain'] = domain
        return self.request(DOMAIN_CREATE_URL,req_data)


    def remove_domain(self, domain_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        return self.request(DOMAIN_REMOVE_URL,req_data)

    def get_domain_list(self):
        req_data = self.values.copy()
        req_data['type'] = 'mine'
        req_data['offset'] = '0'
        req_data['length'] = '3000'
        return self.request(DOMAIN_LIST_URL,req_data)

    def get_domain_log(self,domain_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['offset'] = '0'
        req_data['length'] = '500'
        return self.request(DOMAIN_LOG_URL,req_data)

    def get_domain_info(self, domain_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        return self.request(DOMAIN_INFO_URL,req_data)

    def enable_domain(self,domain_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['status'] = 'enable'
        return self.request(DOMAIN_STATUS_URL,req_data)

    def disable_domain(self,domain_id):
        req_data = self.values.copy()
        req_data['domain_id'] = domain_id
        req_data['status'] = 'disable'
        return self.request(DOMAIN_STATUS_URL,req_data)

    def get_domain_group_list(self):
        return self.request(DOMAIN_GROUP_LIST_URL,self.values)

    def create_domain_group(self,group_name):
        req_data = self.values.copy()
        req_data['group_name'] = group_name
        self.request(DOMAIN_GROUP_CREATE_URL,req_data)

    def modify_domain_group(self,group_id,group_name):
        req_data = self.values.copy()
        req_data['group_id']   = group_id
        req_data['group_name'] = group_name
        self.request(DOMAIN_GROUP_MODIFY_URL,req_data)

    def remove_domain_group(self,group_id):
        req_data = self.values.copy()
        req_data['group_id']   = group_id
        self.request(DOMAIN_GROUP_REMOVE_URL,req_data)

    def change_domain_group(self,domain_id,group_id):
        req_data = self.values.copy()
        req_data['group_id']   = group_id
        req_data['domain_id'] = domain_id
        self.request(DOMAIN_GROUP_CHANGE_URL,req_data)
