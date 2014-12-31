#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        Isilon Tools
# Purpose:     Backup and restore NFS exports on Isilon using RESTful services.
#
# Author:      Tamir Obergot
#              Delivery specialist, EMC
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
from isilon import session
import platform
from .exceptions import ObjectNotFound, APIError, ConnectionError


class API(object):

    def __init__(self, clustername, username, password, services=["platform", "namespace"]):
        self.session = session.Session(clustername, username, password, services)
        self.platform = platform.Platform(self.session)