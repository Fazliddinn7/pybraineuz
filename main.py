from pybrainuz.app import PyBrainApp
from pybrainuz.middleware import Middleware

app = PyBrainApp()


@app.route('/home', allowed_methods=['get'])
def home(request, response):
    response.text = "Hello from the Home page"


@app.route('/about', allowed_methods=["put"])
def about(request, response):
    response.text = "Hello from the About page"


@app.route('/hello/{name}')
def greeting(request, response, name):
    response.text = f'Hello {name}'


@app.route('/books')
class Books:
    def get(self, request, response):
        response.text = "Books page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"


def new_handler(req, resp):
    resp.text = 'From new handler'


app.add_route('/new-handler', new_handler)


@app.route('/template')
def template_handler(req, resp):
    resp.html = app.template(
        'home.html',
        context={
            "new_title": "New title",
            "new_body": "New body 123",
        }
    )


@app.route('/json')
def json_handler(req, resp):
    response_data = {'name': 'some name', 'type': 'json'}
    resp.json = response_data


def on_exception(req, resp, exc_class):
    resp.text = str(exc_class)


app.add_exception_handler(on_exception)


@app.route('/exception')
def exception_throwing_handler(req, resp):
    raise AttributeError('some exception')


class LoggingMiddleware(Middleware):

    def proccess_request(self, req):
        print("request is being called")

    def proccess_response(self, req, resp):
        print("response has been generated")


app.add_middleware(LoggingMiddleware)
