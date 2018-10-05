import requests
import redis
import socket
import configparser

from threading import Thread

config = configparser.ConfigParser()
config.read('../config.ini')

def resolve(target, subdomain):
    try:
        r = redis.StrictRedis(host=config['DEFAULT']['redis_host'], port=int(config['DEFAULT']['redis_port']), db=0)
        check = socket.gethostbyname("%s.%s" % (subdomain, target))
        if not r.exists("%s.%s" % (subdomain, target)):
            r.set("%s.%s" % (subdomain, target), check)
            r.publish("domains", "%s.%s,%s" % (subdomain, target, check))
	return
    except Exception:
        pass

with open("../targets.txt", "r") as targets:
    targets = [target.strip() for target in targets]

with open("../wordlist.txt", "r") as domains:
    domains = [domain.strip() for domain in domains]

for target in targets:
    for subdomain in domains:
        t = Thread(target=resolve, args=(target,subdomain))
        t.start()
