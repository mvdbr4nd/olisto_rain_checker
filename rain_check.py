#!/usr/bin/python3

import requests
import sys
import os
import json
import time
import logging
from logging.handlers import RotatingFileHandler
from urllib import request as req
from urllib import parse
import traceback
from config import Config

config = Config()

logger = logging.getLogger(__name__)

def urlencode(str):
    return parse.quote(str)

def speak(string):
    if config.config["speak_enabled"]:
        try:
            url = "%s%s"%(config.config["speak_url"], urlencode(string))
            print(url)
            rq = req.Request(url)
            req.urlopen(rq)
        except:
            traceback.print_exc()
            pass

def rain_score_text(rain_score):
    if rain_score > 10:
        return 'Very light rain'
    if rain_score > 70:
        return 'Light rain'
    if rain_score > 110:
        return 'Persistent rain'
    if rain_score > 135:
        return 'Heavy rain'
    if rain_score > 165:
        return 'Very heavy rain'
    return 'Dry'

def check_rain():
    global last_rain_score

    rain_url_loc = config.config['api_url'] + "lat=%s&lon=%s"%(config.config['latitude'], config.config['longitude'])
    page = requests.get(rain_url_loc)

    if page.status_code == 200:
        b_data = page.text.split()
        rain_score = 0
        for item in b_data[:3]:
            try:
                rainscore, _time = item.split('|')
                rain_score = max(int(rain_score), int(rainscore))
                #print("rainscore: %s"%rainscore)
            except:
                logger.error("Failed to parse Buienradar response")
                pass

        if config.config['pilight_enabled']:
            try:
                os.system("pilight-send -p generic_label -i %s -l '%s, %s'"%(config.config['pilight_label'], rain_score_text(rain_score), rain_score))

            except:
                logger.error("Failed to update pilight")
                pass

        if rain_score != last_rain_score:
            logger.debug("Got new rain score %s"%rain_score)
            if rain_score > 60:
                speak("incoming %s detected"%rain_score_text(rain_score))

            last_rain_score = rain_score
            # post rain score to Olisto
            url = '%s?value=%s'%(config.config['olisto_connector'], rain_score)
            requests.post(url)
    else:
        logger.error("Cannot update rain data failed to get buienradar response")

last_rain_score = 0

if __name__ == '__main__':
    handler = RotatingFileHandler(
        'rain_check.log',
        maxBytes=100000,
        backupCount=30)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)-22s - %(levelname)-8s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler_stdout = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler_stdout)
    logger.setLevel(logging.DEBUG)

    logger.info("Starting Olisto Rain checker")
    while True:
        check_rain()
        time.sleep(config.config['interval'])
