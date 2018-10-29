#!/usr/bin/python
import requests

base_url = 'http://192.168.0.4:82'
turn_on_endpoint = '/on'
turn_off_endpoint = '/off'
status_endpoint = '/status'

def make_request(url):
    """Makes web request to specified url. Returns response text"""
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as e:
        return 'error' + str(e)
    return req.text.replace('\n', '')

print make_request(base_url + turn_off_endpoint)
