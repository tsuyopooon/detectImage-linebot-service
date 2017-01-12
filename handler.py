# coding:utf-8
# !/usr/bin/python

import json
import logging

import line

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def callback(event, context):
    logger.debug('event: ' + json.dumps(event))

    headers = event.get('headers')
    logger.debug('headers: ' + json.dumps(headers))
    body = event.get('body').decode('utf-8')
    logger.debug('body: ' + body)

    line.reply(headers, body)
