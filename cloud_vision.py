# coding:utf-8

import os
import sys
import base64
import json
import logging

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vendor'))

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

def detect_image(image_content):
    service = get_vision_service()

    image_content = base64.b64encode(image_content)
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [
                {'type': 'LABEL_DETECTION', 'maxResults': 5},
                {'type': 'FACE_DETECTION', 'maxResults': 5},
                {"type": "SAFE_SEARCH_DETECTION", "maxResults": 5}
            ],
            'imageContext': {
                'languageHints': [
                    "ja",
                    "en"
                ]
            }
        }]
    })

    try:
        result = service_request.execute()
        logger.info('result: ' + json.dumps(result))

        return parse(result)
    except Exception as e:
        logger.error(e)
        return 'パニクってる、なう'

def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build(
            'vision', 'v1', credentials=credentials,
            discoveryServiceUrl=DISCOVERY_URL)

def parse(response):
    target_likeLihood = ["POSSIBLE", "LIKELY", "VERY_LIKELY"]

    text = ''
    annotations = response.get('responses')[0].get('labelAnnotations')
    if annotations != None:
        text += u'こんな感じの写真だね!' + os.linesep
        for annotation in annotations:
            text += u'[ ' + annotation.get("description") + u' ]' + os.linesep
        text += os.linesep

    annotations = response.get('responses')[0].get('faceAnnotations')
    if annotations != None:
        for annotation in annotations:
            isLikeLihood = False
            if annotation.get("joyLikelihood") in target_likeLihood:
                text += u"楽しんでる！"
                isLikeLihood = True
            if annotation.get("sorrowLikelihood") in target_likeLihood:
                text += u"悲しそう...な"
                isLikeLihood = True
            if annotation.get("angerLikelihood") in target_likeLihood:
                text += u"オコな"
                isLikeLihood = True
            if annotation.get("surpriseLikelihood") in target_likeLihood:
                text += u"びっくりしてる"
                isLikeLihood = True
            if annotation.get("underExposedLikelihood") in target_likeLihood:
                text += u"露出狂の"
            if annotation.get("blurredLikelihood") in target_likeLihood:
                text += u"ピンボケしちゃってる"
            if annotation.get("headwearLikelihood") in target_likeLihood:
                text += u"帽子好きな"
            if not isLikeLihood:
                text += u"無表情？な"
            text += u"人" + os.linesep
        text += u'の' + str(len(annotations)) + u"人がいるように私には見えます" + os.linesep
        text += os.linesep

    annotation = response.get('responses')[0].get('safeSearchAnnotation')
    if annotation != None:
        if annotation.get("adult") in target_likeLihood:
            text += u"でも、ちょっとエロくない？"
        if annotation.get("medical") in target_likeLihood:
            text += u"でも、グロいのはちょっと..."
        if annotation.get("spoof") in target_likeLihood:
            text += u"でも、パクるのはよくないですよー"
        if annotation.get("violence") in target_likeLihood:
            text += u"でも、私は暴力反対です！"

    logger.debug('text: ' + text)
    return text
