#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko, sys,csv
import time
import getpass

hostname = input('console server IP:')
username = input('username:')
password = getpass.getpass('password:')

port_list = 'PORT_LIST.csv'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def cmd_list(port_number, port_name, port_ip):
    cmd1 = 'cd /ports/serial_ports'
    cmd2 = 'set_cas ' + str(port_number)
    cmd3 = 'set status=enabled'
    cmd4 = 'cd cas'
    cmd5 = 'set port_name=' + str(port_name)
    cmd6 = 'set port_ipv4_alias=' + str(port_ip)
    cmd7 = 'save'
    return cmd1 + ';' + cmd2 + ';' + cmd3 + ';' + cmd4  + ';' + cmd5 + ';' + cmd6 + ';' + cmd7 + ';'

with open(port_list) as f:
    reader = csv.reader(f)
    for row in reader:
        cmds = cmd_list (row[0],row[1],row[2])
        print ("the command is: " + cmds)
        client.connect(hostname= hostname,port=22,username=username,password=password)
        stdin,stdout,stderr = client.exec_command(cmds)
        print (stdout.readlines())
        print (stderr.readlines())
        print ("port " + row[0] + " " + row[1] +" IP " + row[2] +" has been configured")
        #time.sleep(2)
        client.close()
