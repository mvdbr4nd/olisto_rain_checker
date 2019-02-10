#!/usr/bin/python3

import requests
import sys
import os
import json
import time
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

def check_rain(data):
    rain_url_loc = data['api_url'] + "lat=%s&lon=%s"%(data['latitude'], data['longitude'])
    page = requests.get(rain_url_loc)

    if page.status_code == 200:
        b_data = page.text.split()
        rain_score = 0
        for item in b_data[:3]:
            try:
                rainscore, _time = item.split('|')
                rain_score = max(int(rain_score), int(rainscore))
            except:
                logger.error("Failed to parse Buienradar response")
                pass

        if data['pilight_enabled']:
            try:
                rain_desc = 'Dry'
                if rain_score > 10:
                    rain_desc = 'Very light rain'
                if rain_score > 70:
                    rain_desc = 'Light rain'
                if rain_score > 110:
                    rain_desc = 'Persistent rain'
                if rain_score > 135:
                    rain_desc = 'Heavy rain'
                if rain_score > 165:
                    rain_desc = 'Very heavy rain'

                os.system("pilight-send -p generic_label -i %s -l '%s, %s'"%(data['pilight_label'], rain_desc, rain_score))

            except:
                logger.error("Failed to update pilight")
                pass

        if rain_score != check_rain.last_rain_score:
            logger.debug("Got new rain score %s"%rain_score)
            check_rain.last_rain_score = rain_score
            # post rain score to Olisto
            url = '%s?value=%s'%(data['olisto_connector'], rain_score)
            requests.post(url)
    else:
        logger.error("Cannot update rain data failed to get buienradar response")

check_rain.last_rain_score = 0

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

    logger.info("Loading configuration")

    try:
        with open('rain_check.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        logger.error("Failed to open configuration, create the configuration file: rain_check.json")
        sys.exit()
    except ValueError:
        logger.error("Failed to parse configuration")
        sys.exit()

    logger.info("Starting Olisto Rain checker")
    while True:
        check_rain(data)
        time.sleep(data['interval'])
