#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,re,sys,subprocess,time

iface='bond0'

try:
    iface_oper=open('/sys/class/net/'+iface+'/operstate','r')
except:
    print '%s not exist' % (iface)
    print '%s not exist' % (iface)
    print '#FF0000'
    sys.exit()

iface_state=iface_oper.readline()[:-1]
if iface_state=='down':
    print '%s down' % (iface)
    print '%s down' % (iface)
    print '#FF0000'
    sys.exit()

#find address on iface
address_command=subprocess.Popen(['ip','a','sh','dev',iface],stdout=subprocess.PIPE)
search=False
for line in address_command.stdout.readlines():
    if search: continue
    address_test=re.search('\s+inet6*\s+([0-9a-f\.:]*)/[0-9]+\s+.*scope\s+global',line)
    if address_test:
        address=address_test.group(1)
        search=True

#rate for rx and tx
test_olddata=os.path.isfile('/dev/shm/net-'+iface)
rxfile=open('/sys/class/net/'+iface+'/statistics/rx_bytes','r')
txfile=open('/sys/class/net/'+iface+'/statistics/tx_bytes','r')
rx=int(rxfile.readline()[:-1])
tx=int(txfile.readline()[:-1])
date=int(time.strftime('%s',time.gmtime()))
if test_olddata:
    oldfile=open('/dev/shm/net-'+iface,'r+')
    line = oldfile.readline()
    try:
        olddate, oldrx, oldtx = line.split(' ')    
    except:
        olddate=0
        oldrx=0
        oldtx=0
    oldfile.seek(0,0)
else:
    oldfile=open('/dev/shm/net-'+iface,'w')
    olddate=date
    oldtx=tx
    oldrx=rx
oldfile.write('%d %d %d' % (date,rx,tx))
oldfile.close()

date_length=date-int(olddate)
rx_length=rx-int(oldrx)
tx_length=tx-int(oldtx)
rxbytes=float(rx_length)/date_length
txbytes=float(tx_length)/date_length

#unit for rx and tx
rxunit='B'
if rxbytes>1024:
    rxbytes=rxbytes/1024
    rxunit='KB'
    if rxbytes>1024:
        rxbytes=rxbytes/1024
        rxunit='MB'
txunit='B'
if txbytes>1024:
    txbytes=rxbytes/1024
    txunit='KB'
    if txbytes>1024:
        txbytes=rxbytes/1024
        txunit='MB'

print u'%s %5.1f%s /%5.1f%s' % (address,rxbytes,rxunit,txbytes,txunit)
print u'%s %5.1f%s /%5.1f%s' % (address,rxbytes,rxunit,txbytes,txunit)
#print '#00FF00'
