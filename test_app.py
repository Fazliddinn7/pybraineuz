import pytest
import json
from pybrainuz.middleware import Middleware


def test_basic_route_adding(app):
    @app.route('/home')
    def home(req, resp):
        resp.text = "Hello from home"


def test_duplicate_routes_throws_exception(app):
    @app.route('/home')
    def home(req, resp):
        resp.text = 'Hello from home'

    with pytest.raises(AssertionError):
        @app.route('/home')
        def home2(req, resp):
            resp.text = 'Hello from home2'


def test_requests_can_be_sent_by_test_client(app, test_client):
    @app.route('/home')
    def home(req, resp):
        resp.text = "Hello from home"

    response = test_client.get('http://testserver/home')

    assert response.text == "Hello from home"


def test_parameterized_routing(app, test_client):
    @app.route('/hello/{name}')
    def greeting(req, resp, name):
        resp.text = f'Hello {name}'

    assert test_client.get('http://testserver/hello/Fazliddin').text == "Hello Fazliddin"
    assert test_client.get('http://testserver/hello/Islom').text == "Hello Islom"


def test_default_response(test_client):
    response = test_client.get('http://testserver/nimadr')

    assert response.text == "Not Found."
    assert response.status_code == 404


def test_class_based_get(app, test_client):
    @app.route('/books')
    class Books:
        def get(self, req, resp):
            resp.text = "Books page"

    assert test_client.get('http://testserver/books').text == "Books page"


def test_class_based_post(app, test_client):
    @app.route('/books')
    class Books:
        def post(self, req, resp):
            resp.text = "Endpoint to create book."

    assert test_client.post('http://testserver/books').text == "Endpoint to create book."


def test_class_based_method_not_allowed(app, test_client):
    @app.route('/books')
    class Books:
        def post(self, req, resp):
            resp.text = "Endpoint to create book."

    response = test_client.get('http://testserver/books')

    assert response.text == "Method Not Allowed"
    assert response.status_code == 405


def test_alternative_route_adding(app, test_client):
    def new_handler(req, resp):
        resp.text = 'From new handler'

    app.add_route('/new-handler', new_handler)

    assert test_client.get('http://testserver/new-handler').text == 'From new handler'


def test_template_handler(app, test_client):
    @app.route('/test-templates')
    def template(req, resp):
        resp.body = app.template(
            "test.html",
            context={
                'new_title': "Best title",
                'new_body': "Best body",
            }
        )

    response = test_client.get('http://testserver/test-templates')

    assert "Best body" in response.text
    assert "Best title" in response.text
    assert 'text/html' in response.headers['Content-Type']


def test_custom_exception_handler(app, test_client):
    def on_exception(req, resp, exc_class):
        resp.text = "Somthing bad happened"

    app.add_exception_handler(on_exception)

    @app.route('/exception')
    def exception_throwing_handler(req, resp):
        raise AttributeError('some exception')

    response = test_client.get('http://testserver/exception')

    assert response.text == "Somthing bad happened"


def test_non_existent_static_file(test_client):
    assert test_client.get('http://testserver/static/noneexistent.css').status_code == 404


def test_serving_static_file(test_client):
    response = test_client.get('http://testserver/static/test.css')

    assert response.text == "body { background-color: blue;}"


def test_middleware_methods_are_called(app, test_client):
    proccess_request_called = False
    proccess_response_called = False

    class SimpleMiddleware(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def proccess_request(self, req):
            nonlocal proccess_request_called
            proccess_request_called = True

        def proccess_response(self, req, resp):
            nonlocal proccess_response_called
            proccess_response_called = True

    app.add_middleware(SimpleMiddleware)

    @app.route("/home")
    def index(req, resp):
        resp.text = "from handler"

    test_client.get("http://testserver/home")

    assert proccess_request_called is True
    assert proccess_request_called is True


def test_allowed_methods_for_function_based_handler(app, test_client):
    @app.route("/home", allowed_methods=["post"])
    def home(req, resp):
        resp.text = "Hello from home"

    resp = test_client.get("http://testserver/home")

    assert resp.status_code == 405
    assert resp.text == "Method Not Allowed"


def test_json_response_helper(app, test_client):
    @app.route("/json")
    def json_handler(req, resp):
        resp.json = {"name": "pybraineuz"}

    response = test_client.get("http://testserver/json")
    resp_data = response.json()

    assert response.headers["Content-type"] == 'application/json'
    assert resp_data['name'] == 'pybraineuz'


def test_text_response_helper(app, test_client):
    @app.route("/text")
    def text_handler(req, resp):
        resp.text = 'plain text'

    resp = test_client.get('http://testserver/text')

    assert 'text/plain' in resp.headers['Content-type']
    assert resp.text == 'plain text'


def test_html_response_helper(app, test_client):
    @app.route('/html')
    def html_handler(req, resp):
        resp.html = app.template(
            "test.html",
            context={
                "new_title": "Best Title",
                "new_body": "Best Body",
            }
        )

    response = test_client.get('http://testserver/html')

    assert 'text/html' in response.headers['Content-type']
    assert "Best Title" in response.text
    assert "Best Body" in response.text
