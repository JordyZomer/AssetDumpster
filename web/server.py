import tornado.ioloop
import tornado.web
import validators
import redis
import tornado.options
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

tornado.options.parse_command_line()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        domain = self.get_argument("domain", None)
	if domain is None:
		return self.render("search.html", results=None)
	if not validators.domain(domain):
		return self.write({"status": "error, not a valid domain try removing any wildcards!"})
	r = redis.StrictRedis(host=config['DEFAULT']['redis_host'], port=int(config['DEFAULT']['redis_port']), db=0)
	output = r.keys("*." + domain)
	keys = [r.get(x) for x in output]
	d = {key: value for (key, value) in zip(output, keys)}
	return self.render("search.html", results=d)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/search", SearchHandler),
	(r"/css/(style.\css)",tornado.web.StaticFileHandler, {"path": "./css"},),
	(r"/(favicon.\ico)",tornado.web.StaticFileHandler, {"path": "./"},),
	(r"/scripts/(jquery.\js)",tornado.web.StaticFileHandler, {"path": "./scripts"},),
	(r"/scripts/(app.\js)",tornado.web.StaticFileHandler, {"path": "./scripts"},),
    ])

if __name__ == "__main__":
    app = tornado.httpserver.HTTPServer(make_app())
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
