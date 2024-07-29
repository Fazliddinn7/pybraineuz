from webob import Request


class Middleware:
    def __init__(self, app):
        self.app = app

    def add(self, middleware_class):
        self.app = middleware_class(self.app)

    def proccess_request(self, req):
        pass

    def proccess_response(self, req, resp):
        pass

    def handle_request(self, req):
        self.proccess_request(req)
        response = self.app.handle_request(req)
        self.proccess_response(req, response)

        return response

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)
