#!/usr/bin/env python
import io
import os
import re
import sys
import json
import subprocess
import requests
import ipaddress
import hmac
from hashlib import sha1
from flask import Flask, request, abort
import tutum


"""
Conditionally import ProxyFix from werkzeug if the USE_PROXYFIX environment
variable is set to true.  If you intend to import this as a module in your own
code, use os.environ to set the environment variable before importing this as a
module.

.. code:: python

    os.environ['USE_PROXYFIX'] = 'true'
    import flask-github-webhook-handler.index as handler

"""
if os.environ.get('USE_PROXYFIX', None) == 'true':
    from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.debug = os.environ.get('DEBUG') == 'true'
SERVICE_MAP = json.loads(os.environ.get('SERVICE_MAP'))

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'OK'
    elif request.method == 'POST':
        # Store the IP address of the requester
        request_ip = ipaddress.ip_address(u'{0}'.format(request.remote_addr))

        # If GHE_ADDRESS is specified, use it as the hook_blocks.
        if os.environ.get('GHE_ADDRESS', None):
            hook_blocks = [os.environ.get('GHE_ADDRESS')]
        # Otherwise get the hook address blocks from the API.
        else:
            hook_blocks = requests.get('https://api.github.com/meta').json()[
                'hooks']

        # Check if the POST request is from github.com or GHE
        foundIp = False
        for block in hook_blocks:
            if ipaddress.ip_address(request_ip) in ipaddress.ip_network(block):
                foundIp = True;
                break  # the remote_addr is within the network range of github.

        if not foundIp:
            abort(403)

        if request.headers.get('X-GitHub-Event') == "ping":
            return json.dumps({'msg': 'Pong!'})
        if request.headers.get('X-GitHub-Event') != "push":
            return json.dumps({'msg': "Cannot handle event type: " + str(request.headers.get('X-GitHub-Event'))})

        payload = json.loads(request.data)
        match = re.match(r"refs/heads/(?P<branch>.*)", payload['ref'])
        if match:
            branch = match.groupdict()['branch']
            service_id = SERVICE_MAP[branch]
            service = tutum.Service.fetch(service_id)
            service.redeploy()
            return 'OK'
        else:
            abort(500)

# Check if python version is less than 2.7.7
if sys.version_info < (2, 7, 7):
    # http://blog.turret.io/hmac-in-go-python-ruby-php-and-nodejs/
    def compare_digest(a, b):
        """
        ** From Django source **

        Run a constant time comparison against two strings

        Returns true if a and b are equal.

        a and b must both be the same length, or False is
        returned immediately
        """
        if len(a) != len(b):
            return False

        result = 0
        for ch_a, ch_b in zip(a, b):
            result |= ord(ch_a) ^ ord(ch_b)
        return result == 0
else:
    compare_digest = hmac.compare_digest

if __name__ == "__main__":
    try:
        port_number = int(sys.argv[1])
    except:
        port_number = 80
    if os.environ.get('USE_PROXYFIX', None) == 'true':
        app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0', port=port_number)
