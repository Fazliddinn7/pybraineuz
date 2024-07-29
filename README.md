# PyBraineUZ: Python Web Framework built for learning purposes

![purpose](https://img.shields.io/badge/purpose-learning-green)

![PyPI - Version](https://img.shields.io/pypi/v/pybraineuz)

PyBraineUz is a Python web framework built for learning purpose.

It's a WSGI framework and can be used with any WSGI application server such as Gunicorn.

## Installation

```shel
pip install pybraineuz
```

## How to use it

### Basic usage:

```python
from pybarineuz.app import PyBraineUz

app = PyBraineUz()


@app.route('/home', allowed_methods=['get'])
def home(request, response):
    response.text = "Hello from the Home page"


@app.route('/hello/{name}')
def greeting(request, response, name):
    response.text = f'Hello {name}'


@app.route('/books')
class Books:
    def get(self, request, response):
        response.text = "Books page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"


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
```

### Unit Tests

The recommended way of writing unit tests is with [pytest](http://docs.pytest.org/en/latest/). There are two built in
fixture that you may want to use when writing unit tests with PyBraineUz. The first one is `app` which is an instance of
the main `API` class:

```python
def test_route_overlap_throws_exception(app):
    @route('/')
    def home(req, resp):
        resp.text = "Welcome home."

    with pytest.raises(AssertionError):
        @app.route('/')
        def home2(req, resp):
            resp.text = "Welcome home2."
```

The other one is `client` that you can use to send HTTP requests to your handlers. It is based on the
famous [requests](http://requests.readthedics.io/) and it should feel very familiar:

```python
def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
```

## Templates

The default folder for templates is `templates`. You can change it when initializing the main `API()` class:

```python
app = API(templates_dir="templates_dor_name")
```

When you can use HTML files in that folder like so in a handler:

```python
@app.route("/show/template")
def handler_with_template(req, resp):
    resp.html = app.template(
        "example.html", context={
            "title": "Awesome Framework",
            "body": "welcome to the future!"
        }
    )
```

## Static Files

Just like templates, the default folder for static files is `static` and you can override it:

```python
app = API(static_dir="static_dir_name")
```

Then you can use the files inside this folder in HTML files:

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
</head>

<body>
<h1>{{body}}</h1>
<p>This is a paragraph</p>
</body>
</html>
```

### Middleware

You can create custom middleware classes by inheriting from the `pybraineuz.middleware. Middleware` class and overriding
its two methods that are called before and after each requests:

```python
from pybraineuz.api import API
from pybraineuz.middleware import Middleware

app = API()


class SimpleCustomMiddleware(Middleware):

    def proccess_request(self, req):
        print("Before dispatch", req.url)

    def proccess_response(self, req, resp):
        print("After dispatch", req.url)


app.add_middleware(SimpleCustomMiddleware)
```










