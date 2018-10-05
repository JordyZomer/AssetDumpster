import redis
import simplemail
import configparser

from jinja2 import Environment

config = configparser.ConfigParser()
config.read('../config.ini')

r = redis.StrictRedis(host=config['DEFAULT']['redis_host'], port=int(config['DEFAULT']['redis_port']), db=0)
pubsub = r.pubsub()
pubsub.subscribe(['domains'])

targets = []
for item in pubsub.listen():
    print(item["data"])
    targets.append(item["data"])
    if len(targets) == 2:
        try:
	    message = """
	    Hey user!

	    New assets have been discovered! 
	    {% for target in targets %}
		{{ target }}
	    {% endfor %}

	    Happy hacking!

	    AssetDumpster
	    """
	    message = Environment().from_string(message).render(email=email.strip(), targets=targets[1:])
	    simplemail.Email(
	    smtp_server = "localhost",
	    from_address = config['DEFAULT']['sender_address'],
	    to_address = config['DEFAULT']['recipient_address'],
	    subject = "New targets found!",
	    message = message,
	    ).send()
	    del targets[:]
        except Exception:
            raise
            pass
