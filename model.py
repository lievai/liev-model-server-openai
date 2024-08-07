import os
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
import json
from config.config import Config
import openai
import logging
from dotenv import load_dotenv

load_dotenv()

# Initialize logging to console - do not use file appenders in container mode
logging.basicConfig(level=os.getenv('LOG_LEVEL', default= 'INFO'), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info('STARTING model.py')


config = Config('openai')

LIEV_PASSWORD = config.get("LIEV_PASSWORD")
LIEV_USERNAME = config.get("LIEV_USERNAME")

MODEL = config.get("MODEL")

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    """ Verify: Check username and password to allow access to the API"""
    if not (username and password):
        return False
    return username == LIEV_USERNAME and password == LIEV_PASSWORD


@app.route('/response')
@auth.login_required
def response():

    openai.api_key = config.get("OPENAI_KEY")
    
    data = request.data
    try:
        data = json.loads(data)
    except Exception as e:
        logger.error(f"JSON load problem!: {e}", exc_info=True)
        return json.dumps("JSON load problem !"), 500

    if isinstance(data, dict) == False:
        return json.dumps("JSON load conversion problem. Not a dict ! Are you using data payload  ?"), 400
    
    temperature = float(data.get('temperature', 1))
    top_p = float(data.get('top_p', 1))
    stop_words = data.get('stop_words', [])

    # verifica se existe a chave messages no dict:
    if data.get('messages'):
        # se existir, verifica se existe instruction ou system_msg juntos
        if data.get('instruction') or data.get('system_msg'):
            return json.dumps("If the messages parameter is passed, the instruction or system_msg parameters must not be passed."), 501
        messages = data['messages']
    else:
        instruction = data.get('instruction', "hi")
        system_msg = data.get('system_msg', None)
        history = data.get('history', [])

        messages = []
        for h in history:
            messages.append({"role": "user", "content": h[0]})
            messages.append({"role": "assistant", "content": h[1]})
        if system_msg != None:
            messages.append({"role": "system", "content": system_msg})
        messages.append({"role": "user", "content": instruction})

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            temperature=temperature,
            top_p=top_p,
            messages=messages,
            stop=stop_words
        )
        answer = response.choices[0]['message']['content']
        return json.dumps(answer), 200
    except Exception as e:
        answer = "Error ! : " + str(e)
        logger.error(answer, exc_info=True)
        return json.dumps(answer), 500


# DO NOT REMOVE
@app.route('/healthz')
def liveness():
    # You can add custom logic here to check the application's liveness
    # For simplicity, we'll just return a 200 OK response.
    return json.dumps({'status': 'OK'})

# DO NOT REMOVE
# Health check endpoint for readiness probe
@app.route('/readyz')
def readiness():
    # You can add custom logic here to check the application's readiness
    # For simplicity, we'll just return a 200 OK response.
    return json.dumps({'status': 'OK'})
