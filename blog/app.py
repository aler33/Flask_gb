from flask import Flask, request, g
from time import time


app = Flask(__name__)


@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


@app.route("/")
def index():
    return "Hello web!"


@app.route("/test/<name_1>/")
def greet_name(name_1: str):
    return f'Hello {name_1}!'


@app.route("/user/")
def read_user():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"


@app.route("/status/", methods=["GET", "POST"])
def custom_status_code():
    if request.method == "GET":
        return """\
        To get response with custom status code
        send request using POST method
        and pass `code` in JSON body / FormData
        """

    print("raw bytes data:", request.data)

    if request.form and "code" in request.form:
        return f'"code from form", {request.form["code"]}'

    if request.json and "code" in request.json:
        return f'"code from json", {request.json["code"]}'

    return f'"", 204'


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time

    return response
