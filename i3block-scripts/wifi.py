#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,re,sys,subprocess

iface='wlp3s0'

try:
    iface_oper=open('/sys/class/net/'+iface+'/operstate','r')
except:
    print('%s not exist' % (iface))
    print('%s not exist' % (iface))
    print('#FF0000')
    sys.exit()

iface_state=iface_oper.readline()[:-1]
if iface_state=='down':
    print('%s down' % (iface))
    print('%s down' % (iface))
    print('#FF0000')
    sys.exit()

#find ESSID
essid=''
linkq=0
iwconfig_command=subprocess.Popen(['/sbin/iwconfig',iface],stdout=subprocess.PIPE)
for line in iwconfig_command.stdout.readlines():
    #print('line: %s' % line)
    iwconfigre=re.search('ESSID:"([^"]*)"',line.decode("utf-8"))
    if iwconfigre:
        essid=iwconfigre.group(1)
    linkqre=re.search('Link Quality=([0-9]*)/',line.decode("utf-8"))
    if linkqre:
        linkq=int(linkqre.group(1))

link=linkq*100/70
print(u'%d%% %s' % (link,essid))
print(u'%d%% %s' % (link,essid))
#color
if  link>=80:
    print('#00FF00')
elif link>=60:
    print('#FFF600')
elif link>=40:
    print('#FFAE00')
else:
    print('#FF0000')
