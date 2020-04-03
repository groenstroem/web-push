import json
import logging
import sqlite3
import time
from urllib.parse import urlparse

from pywebpush import WebPusher
from py_vapid import Vapid
import requests


logging.basicConfig(level=logging.DEBUG)

with open('config.json') as config_file:
    config = json.load(config_file)

# Use grønstrøm API to get contents of push message
message = requests.get('https://grønstrøm.nu/api/v1/next-day').text
logging.info(f'Sending push message: {message}')

# Get all subscriptions from SQLite database
conn = sqlite3.Connection('/data/subs.db')
try:
    c = conn.cursor()
    for i, row in enumerate(c.execute('SELECT * FROM subs')):
        try:
            # Manually recreate the push facade from the pywebpush API to be able to specify both TTL and urgency
            subscription_info = json.loads(row[0])
            pusher = WebPusher(subscription_info)
            url = urlparse(subscription_info['endpoint'])
            aud = "{}://{}".format(url.scheme, url.netloc)
            vapid_claims = {'sub': f'mailto:{config["sub_email"]}',
                            'aud': aud,
                            'exp': int(time.time()) + 12 * 60 * 60}
            vv = Vapid.from_string(config['vapid_key'])
            headers = vv.sign(vapid_claims)
            # Define the urgency to be "normal", corresponding to messages being delivered
            # while the device is "On neither power nor wifi".
            # https://tools.ietf.org/html/draft-ietf-webpush-protocol-12#section-5.3
            headers['Urgency'] = 'normal'
            resp = pusher.send(message, headers, ttl=12 * 60 * 60)
            # TODO: Handle cases where response status code is not 201.
            logging.debug(f'{i} ({resp.status_code}: {resp.text}): {subscription_info}')
        except Exception as e:
            logging.warning(f'{i} (failed): {e}')

finally:
    if conn:
        conn.close()

