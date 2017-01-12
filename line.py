# coding:utf-8

import os 
import sys
import json
import logging
import importlib

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vendor'))

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, ImageMessage, TextSendMessage

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
parser = WebhookParser(os.environ['LINE_CHANNEL_SECRET'])

def health_check(headers, body):
    signature = headers.get('X-Line-Signature')
    handler.handle(body, signature)

def reply(headers, body):
    signature = headers.get('X-Line-Signature')

    events = parser.parse(body, signature)

    for event in events:
        if isinstance(event, MessageEvent):
            message = event.message
            if isinstance(message, TextMessage):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='画像よこせ')
                )
            elif isinstance(message, ImageMessage):
                message_content = line_bot_api.get_message_content(event.message.id)

                image_content = ''
                for chunk in message_content.iter_content():
                    image_content += chunk

                module = importlib.import_module(os.environ['DETECT_IMAGE_API'])
                detect = module.detect_image(image_content)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=detect)
                )
