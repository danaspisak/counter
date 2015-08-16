#!/usr/bin/env python
 
import os
import time
import redis
from scapy.all import *
 
#redistogo_url = os.environ['REDISTOGO_URL']
#r = redis.Redis.from_url(redistogo_url)
r = redis.Redis()
os.environ['TZ'] = 'US/Central'
time.tzset()
 
def PacketHandler(pkt) :
        # Look for 802.11 packets
        if pkt.haslayer(Dot11) :
                # narrow it down 
                if pkt.type == 0 and pkt.subtype == 4 :
                        setsize = r.scard('macid')
                        r.sadd('macid',pkt.addr2)
                        newsize = r.scard('macid')
                        if newsize > setsize :
                                setsize = newsize
                                # publish this new size
                                r.publish('count',setsize)
                        # decode the signal strength
                        sig_str = -(256-ord(pkt.notdecoded[-4:-3]))
                        # track the max and min signal strength seen
                        min = r.hget(pkt.addr2, 'min_rssi')                        
                        if sig_str > min :
                            r.hset(pkt.addr2, 'min_rssi', min)
                        
                        max = r.hget(pkt.addr2, 'max_rssi') 
                        if sig_str < max :
                            r.hset(pkt.addr2, 'max_rssi', max)
                        r.hset(pkt.addr2,'rssi',sig_str)
                        r.hincrby(pkt.addr2,'seen',1)
                        r.hset(pkt.addr2,'last_seen',time.strftime('%X %x %Z'))
                        if pkt.info :
                                str = "%s - Client: %s SSID: %s RSSI:%s" % (time.strftime('%X %x %Z'),pkt.addr2, pkt.info,sig_str)
                                print str
                                f = open("clients.log","ab")
                                f.write(str+"\n")
                                f.close()

# store=0 is VERY important so you're not storing the packets and exhausting memory 
sniff(iface="mon0", prn = PacketHandler, store=0)
