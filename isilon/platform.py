#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        Isilon Tools
# Purpose:     Backup and restore NFS exports on Isilon using RESTful services.
#
# Author:      Tamir Obergot
# Delivery specialist, EMC
#              tamir.obergot@emc.com
#
# Version:     2.0
#
# Created:     07.12.2014
#
# Licence:     Open to distribute and modify.  This example code is unsupported
#              by both EMC and the author.  IF YOU HAVE PROBLEMS WITH THIS
#              SOFTWARE, THERE IS NO ONE PROVIDING TECHNICAL SUPPORT FOR
#              RESOLVING ISSUES. USE CODE AS IS!
#
#              THIS CODE IS NOT AFFILIATED WITH EMC CORPORATION.
#-------------------------------------------------------------------------------

import logging
import json


class Platform(object):
    def __init__(self, session):
        self.log = logging.getLogger('logger_agent')
        self.log.addHandler(logging.NullHandler())
        self.session = session
        self.api_call = session.api_call
        self.platform_url = '/platform/1'

    def get_object(self, type):
        objects = ""
        count = 0
        resume = None
        while True:
            if type == 'shares':
                if resume == None:
                    r = self.api_call("GET", self.platform_url + "/protocols/smb/shares")
                else:
                    r = self.api_call("GET", self.platform_url + "/protocols/smb/shares?resume="+resume)
            elif type == 'exports':
                if resume == None:
                    r = self.api_call("GET", self.platform_url + "/protocols/nfs/exports")
                else:
                     r = self.api_call("GET", self.platform_url + "/protocols/nfs/exports?resume="+resume)
            elif type == 'quotas':
                if resume == None:
                    r = self.api_call("GET", self.platform_url + "/quota/quotas/")
                else:
                    r = self.api_call("GET", self.platform_url + "/quota/quotas?resume="+resume)
            else:
                self.log.exception("illegal type!")
            data = r.json()
            for obj in data[type]:
                objects += str(json.dumps(obj)) + "\n"
                if type == 'shares':
                    self.log.log(logging.INFO,"Backing up share on path %s description: %s",obj['path'], obj['description'])
                if type == 'exports':
                    for tmp in obj['paths']:
                        self.log.log(logging.INFO,"Backing up exports on path %s description: %s", tmp, obj['description'])
                if type == 'quotas':
                    self.log.log(logging.INFO,"Backing up quota on path %s type: %s", obj['path'], obj['type'])
                count += 1
            resume = data['resume']
            if resume == None:
                break
        if type in data:
            return objects, count
        return None

    def set_object(self, obj, type):
        if type == 'shares':
            del obj['id']
            params = json.dumps(obj)
            r = self.api_call("POST", self.platform_url + "/protocols/smb/shares", data=params)
        elif type == 'exports':
            del obj['id']
            del obj['time_delta']
            del obj['unresolved_clients']
            del obj['conflicting_paths']
            del obj['map_all']
            params = json.dumps(obj)
            r = self.api_call("POST", self.platform_url + "/protocols/nfs/exports", data=params)
        elif type == 'quotas':
            del obj['usage']
            del obj['linked']
            del obj['ready']
            del obj['id']
            del obj['thresholds']['soft_last_exceeded']
            del obj['thresholds']['hard_last_exceeded']
            del obj['thresholds']['soft_exceeded']
            del obj['thresholds']['hard_exceeded']
            del obj['thresholds']['advisory_last_exceeded']
            del obj['thresholds']['advisory_exceeded']
            del obj['notifications']
            params = json.dumps(obj)
            r = self.api_call("POST", self.platform_url + "/quota/quotas/", data=params)
        return

    def delete_object(self, type):
        if type == 'shares':
            self.log.log(logging.INFO,"Lists all the shares from the Isilon..")
            r = self.api_call("GET", self.platform_url + "/protocols/smb/shares/")
            data = r.json()
            for item in data[type]:
                self.log.log(logging.INFO, "Deleting share "+item['name'])
                r = self.api_call("DELETE", self.platform_url + "/protocols/smb/shares/"+item['name'])

        elif type == 'exports':
            self.log.log(logging.INFO,"Lists all the exports from the Isilon..")
            r = self.api_call("GET", self.platform_url + "/protocols/nfs/exports/")
            data = r.json()
            for item in data[type]:
                self.log.log(logging.INFO, "Deleting export ID: "+str(item['id']))
                r = self.api_call("DELETE", self.platform_url + "/protocols/nfs/exports/"+str(item['id']))

        elif type == 'quotas':
            r = self.api_call("DELETE", self.platform_url + "/quota/quotas/")
            self.log.log(logging.INFO, "Deleting all quotas")
        return
