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
import sys
class ObjectNotFound(RuntimeError):
    """The API has responsed with an HTTP 404 Object not found code"""

class APIError(RuntimeError):
    """This is an api level error"""

class ConnectionError(RuntimeError):
    """This is an api level error"""

class Syntax(Exception):
    def __init__(self, value):
        self.value = value
        sys.tracebacklimit = 0
    def __str__(self):
        return repr(self.value)