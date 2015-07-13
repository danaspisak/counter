#!/usr/bin/env python
 
import os
import time
import redis
from scapy.all import *
 
redistogo_url = os.environ['REDISTOGO_URL']
r = redis.Redis.from_url(redistogo_url)
os.environ['TZ'] = 'US/Central'
time.tzset()
 
def PacketHandler(pkt) :
        if pkt.haslayer(Dot11) :
                if pkt.type == 0 and pkt.subtype == 4 :
                        setsize = r.scard('macid')
                        r.sadd('macid',pkt.addr2)
                        newsize = r.scard('macid')
                        if newsize > setsize :
                                setsize = newsize
                                # public this new size
                                r.publish('count',setsize)
                        sig_str = -(256-ord(pkt.notdecoded[-4:-3]))
                        r.hset(pkt.addr2,'rssi',sig_str)
                        r.hincrby(pkt.addr2,'seen',1)
                        if pkt.info :
                                str = "%s - Client: %s SSID: %s RSSI:%s" % (time.strftime('%X %x %Z'),pkt.addr2, pkt.info,sig_str)
                                print str
                                f = open("clients.log","ab")
                                f.write(str+"\n")
                                f.close()
 
sniff(iface="mon0", prn = PacketHandler, store=0)
