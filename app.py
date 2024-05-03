from flask import Flask, render_template, request
from loguru import logger

from db_helper import db_helper
from services import send_request_to_gpt

app = Flask(__name__)


@logger.catch
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_helper.db_session.remove()


@logger.catch
@app.get("/")
def index():
    return render_template("index.html")


@logger.catch
@app.post("/")
def create_request_to_gpt():
    user_query = request.json["query"]
    gpt_answer = send_request_to_gpt(user_query)

    return dict(gptAnswer=gpt_answer)
