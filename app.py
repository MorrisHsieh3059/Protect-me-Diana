from __future__ import unicode_literals
import errno
import os
import sys
import tempfile
from argparse import ArgumentParser
from flask import Flask, request, abort, jsonify, send_from_directory

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, CarouselTemplate, PostbackEvent,
    StickerMessage, StickerSendMessage, ImagemapSendMessage,
    ImageMessage, ImageSendMessage )

from questionnaire.extract_function import extract, revise_extract       #RE抓數字
from questionnaire.ct_push import ct_push               #抓推播新的carousel template
from questionnaire.confirm import confirm          #抓confirm template 進來
from questionnaire.carousel import *               #抓caousel columns
from questionnaire.confirm_push import confirm_push
from questionnaire.next import next
from questionnaire.imgmap_push import floor_plan
from questionnaire.tempview import takeFirst, tempview, tempview_confirm, cat_tempview, cat_tempview_confirm
from questionnaire.converter import converter
from questionnaire.revise import revise_idiot, revise_confirm, revise_able, cat_revise_confirm
from questionnaire.image_upload import Image_Upload

from account.account_confirm import account_confirm
from account.get_account_db import (
    get_account_db, get_userid_db, delete_userid_db,
    get_school_db, no_repeat_school_db, get_county_db )

from connect.fetch import fetch
from connect.detail import detail
from connect.event import event
from connect.building import building
from connect.overall import overall
# from connect.ner import ner

from db.database import Database

from chat_module.Data import Data
from chat_module.text_process import text_process
from chat_module.postback_process import postback_process
from chat_module.image_process import image_process

DB = Database(os.environ.get('DATABASE_URL'), db_type='postgres')
app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False
data = Data()
line_bot_api = None

account = {} # 帳號設定問問題用的
account_q = 0 # 記住帳號設定的題數

if os.environ.get("FLASK_ENV") == "development":
    line_bot_api = LineBotApi(os.environ.get("TOKEN"), "http://localhost:8080")
else:
    line_bot_api = LineBotApi(os.environ.get("TOKEN"))
handler = WebhookHandler(os.environ.get("SECRET"))

@app.route('/report/<path:name>')
def reportroute(name):
    name = 'index.html' if name is "" else name
    path = os.path.join("report", name)
    with open(path, encoding="utf-8") as f:
        content = f.read()
    return content

def send_js(name):
    return send_from_directory('js', name)

@app.route('/overall')
def overallroute():
    assessment_id = request.args.get('assessment_id')
    return jsonify(overall('{"assessment_id":' + assessment_id + '}', DB))

"""
@app.route('/ner')
def nerroute():
    county = request.args.get('county')
    ass_id  = request.args.get('assessment_id')
    return jsonify(ner('{"county":"' + county + '", "assessment_id":' + ass_id + '}', DB))
"""

@app.route('/event')
def eventroute():
    return jsonify(event(DB))

@app.route('/fetch')
def fetchroute():
    county = request.args.get('county')
    ass_id  = request.args.get('assessment_id')
    return jsonify(fetch('{"county":"' + county + '", "assessment_id":' + ass_id + '}', DB))

@app.route('/building')
def buildingroute():
    school_id = request.args.get('school_id')
    ass_id = request.args.get('assessment_id')
    return jsonify(building('{"school_id":"%s","assessment_id":%s}' % (school_id, ass_id), DB))

@app.route('/detail')
def detailroute():
    ass_id = request.args.get('assessment_id')
    building_id = request.args.get('building_id')
    return jsonify(detail('{"assessment_id":"%s","building_id":"%s"}' % (ass_id, building_id), DB))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] # get X-Line-Signature header value
    body = request.get_data(as_text=True) # get request body as text
    app.logger.info("Request body: " + body)

    try: # handle webhook body
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    userid = event.source.user_id

    ret = text_process(text, userid, data, DB, event)
    if type(ret) != str:
        print(f"text={text}")
        line_bot_api.reply_message(event.reply_token, ret)
    elif ret == "NA":
        print(f"text process did not process.\n    text = {text}")

@handler.add(PostbackEvent)
def handle_postback(event):
    userid = event.source.user_id
    user_data = data.get_user(userid)
    ret = postback_process(userid, data, DB, event)
    global account
    global account_q

    if type(ret) != str:
        line_bot_api.reply_message(event.reply_token, ret)
    elif ret == "NA":
        print(f"postback process did not process.\n    epd = {event.postback.data}")

@handler.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    userid = event.source.user_id
    img_id = event.message.id
    ret = image_process(userid, img_id, data, DB, line_bot_api)

    if type(ret) != str:
        line_bot_api.reply_message(event.reply_token, ret)
    else:
        print(f"img process did not process.\n    img = {img_id}")
