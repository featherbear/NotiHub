# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the MIT License
"""

import builtins
import json
import threading

try:
    import tornado.httputil
    import tornado.ioloop
    import tornado.web
except ModuleNotFoundError:
    host = lambda *_: None

if not hasattr(builtins, "dprint"): dprint = print

WEBSITE_ROOT = "./web_root"
WEBSITE_TEMPLATE = "./web_template"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class APIHandler(tornado.web.RequestHandler):
    def get(self):
        print("API Request")
        request: tornado.httputil.HTTPServerRequest = self.request
        print(request.path)
        print(request.uri)
        print(request.arguments)
        print(json.dumps({}))


def host(port=7080):
    tornado.web.Application([
        ("/api/.*", APIHandler),
        ("/", MainHandler),
        ("/(.*)", tornado.web.StaticFileHandler, {"path": WEBSITE_ROOT}),

    ], template_path=WEBSITE_TEMPLATE).listen(port)
    dprint("Hosting server on port", port)
    tornado.ioloop.IOLoop.current().start()


class WebServer(threading.Thread):
    def run(self, port=None):
        host() if port is None else host(port)


if __name__ == "__main__":
    host()
