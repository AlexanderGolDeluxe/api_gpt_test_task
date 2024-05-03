from loguru import logger
from openai import OpenAI

from config import (
    CHATGPT_API_KEY,
    CHATGPT_MAX_TOKENS,
    CHATGPT_MODEL_ENGINE,
    CHATGPT_TEMPERATURE,
    PROMT_1,
    PROMT_2
)
from db_helper import db_helper
from models import GPTAnswer, UserQuery

client = OpenAI(api_key=CHATGPT_API_KEY)


@logger.catch
def generate_response(text):
    try:
        completion = client.chat.completions.create(
            model=CHATGPT_MODEL_ENGINE,
            max_tokens=CHATGPT_MAX_TOKENS,
            temperature=CHATGPT_TEMPERATURE,
            messages=[dict(role="user", content=text)]
        )
    except Exception as error:
        return dict(error=error.body)

    if completion and completion.choices:
        return completion.choices[0].message.content


@logger.catch
def save_user_query_to_db(query):
    with db_helper.db_session() as session:
        new_user_query = UserQuery(text=query)
        session.add(new_user_query)
        session.commit()

    return new_user_query.id


@logger.catch
def send_request_to_gpt(query):
    user_query_id = save_user_query_to_db(query)
    gpt_answer_one = generate_response(query + PROMT_1)
    if isinstance(gpt_answer_one, dict):
        return gpt_answer_one

    gpt_answer_two = PROMT_2 and generate_response(
        (gpt_answer_one or query) + PROMT_2
    )
    with db_helper.db_session() as session:
        gpt_answer = GPTAnswer(
            user_query_id=user_query_id,
            response_one=gpt_answer_one,
            response_two=gpt_answer_two
        )
        session.add(gpt_answer)
        session.commit()

    return gpt_answer_two or gpt_answer_one
