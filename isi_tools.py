#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        Isilon Tools
# Purpose:     Backup and restore NFS exports on Isilon using RESTful services.
#
# Author:      Tamir Obergot
# Delivery specialist, EMC
# tamir.obergot@emc.com
#
# Version:     2.0
#
# Created:     07.12.2014
#
# Licence:     Open to distribute and modify.  This example code is unsupported
# by both EMC and the author.  IF YOU HAVE PROBLEMS WITH THIS
# SOFTWARE, THERE IS NO ONE PROVIDING TECHNICAL SUPPORT FOR
#              RESOLVING ISSUES. USE CODE AS IS!
#
#              THIS CODE IS NOT AFFILIATED WITH EMC CORPORATION.
#-------------------------------------------------------------------------------
import isilon
import logging.handlers
import logging
import time
import argparse
import json
from isilon.exceptions import Syntax

tm = time.localtime(time.time())
# Set up a specific logger with our desired output level
my_logger = logging.getLogger('logger_agent')

def backup(api, args):
    my_logger.info("Backup operation started on Isilon...")
    if args.type == "all":
        types = ['shares', 'exports', 'quotas']
        for item in types:
            try:
                bckfile = open(
                        './archive/' + item + '_' + str(tm[2]) + '_' + str(tm[1]) + '_' + str(tm[3]) + '_' + str(
                        tm[4]) + '.bck', 'w')
            except:
                my_logger.error("Path not found, opening the backup file in current directory")
                bckfile = open(
                    './' + item + '_' + str(tm[2]) + '_' + str(tm[1]) + '_' + str(tm[3]) + '_' + str(tm[4]) + '.bck', 'w')
            my_logger.info("Opening backup file " + bckfile.name + ".")
            objects = api.platform.get_object(item)
            bckfile.write(objects[0])
            my_logger.info("Total objects: " + str(objects[1]))
            my_logger.info("Closing backup file " + bckfile.name)
    else:
        try:
            bckfile = open(
                    './archive/' + args.type + '_' + str(tm[2]) + '_' + str(tm[1]) + '_' + str(tm[3]) + '_' + str(
                    tm[4]) + '.bck', 'w')
        except:
            my_logger.error("Path not found, opening the backup file in current directory")
            bckfile = open(
                './' + args.type + '_' + str(tm[2]) + '_' + str(tm[1]) + '_' + str(tm[3]) + '_' + str(tm[4]) + '.bck', 'w')
        my_logger.info("Opening backup file " + bckfile.name + ".")
        objects = api.platform.get_object(args.type)
        bckfile.write(objects[0])
        my_logger.info("Total objects: " + str(objects[1]))
        my_logger.info("Closing backup file " + bckfile.name)
    return


def restore(api, args):
    count = 0
    try:
        bckfile = open(args.file, 'r')
    except IOError:
        my_logger.critical("Backup file " + args.file + " doesn't exist!\n")
        raise Exception("Backup file " + args.file + " doesn't exist!")
    my_logger.info("Restore operation started on Isilon...")
    my_logger.info("Opening backup file " + bckfile.name + "...")
    for line in bckfile:
        line = line.replace('\n', '')
        obj = json.loads(line)
        api.platform.set_object(obj, args.type)
        count += 1
    my_logger.info("Total objects: " + str(count))
    my_logger.info("Closing backup file " + bckfile.name + "...")
    my_logger.info("Restore operation to Isilon was finished!")
    return


def delete(api, args):
    my_logger.info("Delete operation started on Isilon...")
    if args.type == "all":
        types = ['shares', 'exports', 'quotas']
        for item in types:
            my_logger.info("Start deleting all "+item)
            objects = api.platform.delete_object(item)
            my_logger.info("Delete operation on Isilon was finished!")
    else:
        my_logger.info("Start deleting all "+args.type)
        objects = api.platform.delete_object(args.type)
        my_logger.info("Delete operation on Isilon was finished!")
    return

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group("Actions")
    group.add_argument('action', help="backup/restore/deletes the object is selected on the --type flag",
                       choices=('backup', 'restore', 'delete'), metavar="backup | delete | restore --file FILE", nargs=1)

    parser.add_argument("-v", "--verbose", help="detailed logging.", action='store_true', required=False )
    group1 = parser.add_argument_group("Required")
    group1.add_argument("-t", "--type", help="specifies the type of the object [shares, export, quotas, all].",
                        action='store', required=True, choices=('shares', 'exports', 'quotas', 'all'), metavar='TYPE')
    group1.add_argument("-f", "--file", help="Path to the backup file for restore operation.", action='store', required=False)
    group1.add_argument("-u", "--username", help="Username for login.", action='store', required=True, dest='user')
    group1.add_argument("-pw", "--password", help="Password to login.", required=True, dest='password')
    group1.add_argument("-n", "--name", help="Cluster name to connect.", action='store', required=True, dest='clustername')
    args = parser.parse_args()

    LOG_FILENAME = args.type + '.log'

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=52428800, backupCount=100)

    # create a logging format
    formatter = logging.Formatter('%(levelname)s %(asctime)s --> %(message)s')
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)

    if args.action[0] == 'restore' and args.file == None:
        my_logger.error("--file is required in restore operation.")
        raise Syntax("--file is required in Restore operation.")
    if args.action[0] == 'restore' and args.type == 'all':
        my_logger.error("--type all is illegal with restore option.")
        raise Syntax("--type all is illegal with restore option.")
    if args.verbose:
        my_logger.setLevel('DEBUG')
    else:
        my_logger.setLevel('INFO')
    my_logger.info('------------------------------------- Isilon Tools -------------------------------------')
    api = isilon.API(args.clustername, args.user, args.password)
    if args.action[0] == 'backup':
        backup(api, args)
    elif args.action[0] == 'restore':
        restore(api, args)
    elif args.action[0] == 'delete':
        delete(api, args)
    my_logger.info("review "+LOG_FILENAME+" for more information.")
main()