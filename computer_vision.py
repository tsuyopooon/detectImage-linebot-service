# coding:utf-8

import os
import json
import logging
import httplib
import urllib
import base64

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

_url = 'https://api.projectoxford.ai/vision/v1/analyses'
_maxNumRetries = 3

def detect_image(image_content):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': os.environ['MICROSOFT_COMPUTER_VISION_KEY'],
    }

    params = urllib.urlencode({
        'visualFeatures': 'Description, Faces, Adult',
    })

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, image_content, headers)

        response = conn.getresponse()
        data = response.read()
        logger.debug('result: ' + data)
        conn.close()
        return parse(json.loads(data))
    except Exception as e:
        logger.error(e)
        return 'パニクってる、なう'


def parse(response):
    text = ''

    description = response.get('description')
    if description is not None:
        captions = description.get('captions')
        if captions:
            text += u'この写真は' + os.linesep
            for caption in captions:
                text += caption.get("text") + os.linesep
            text += u'だね！' + os.linesep

        tags = description.get('tags')
        if tags:
            text += u'勝手にタグ付けしちゃおっと' + os.linesep
            for tag in tags:
                text += u'[ ' + tag + u' ]' + os.linesep
            text += os.linesep

    faces = response.get('faces')
    if faces:
        for face in faces:
            text += str(face.get('age')) + '歳ぐらいの' + face.get('gender') + os.linesep
        text += u'の' + str(len(faces)) + u'人がいるように私には見えます' + os.linesep

    adult = response.get('adult')
    if adult.get('isAdultContent'):
        text += u'でも、ちょっとエロくない？'
    if adult.get('isRacyContent'):
        text += u'あなたいやらしいですね'

    logger.debug('text: ' + text)
    return text
