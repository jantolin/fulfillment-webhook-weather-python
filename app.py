# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 14:22:09 2017

@author: 66472572
"""
from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import requests

from addict import Dict

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "eciStock":
       return {}
    
    url = "https://api.elcorteingles.es/ecommerce/centres?eciReference=001008432115270003&locale=es_ES&provinceECI=28"
    response = urlopen(url)
    data_response = response.read().decode("utf-8")
    
    #result = urlopen(baseurl).read()
    #data = json.loads(result)
    #res = makeWebhookResult(baseurl)
    res = makeWebhookResult(json.loads(data_response))
    return res

#def makeYqlQuery(req):
#    result = req.get("result")
#    parameters = result.get("parameters")
#    city = parameters.get("geo-city")
#    if city is None:
#        return None

#    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    #provinces_eci = data.get('provinces_eci')[0]
       

    #name = stores.get('name')
    #if name is None:
    #    return {}
    # print(json.dumps(item, indent=4))
    

    provinces_eci = data.get('provinces_eci')[0]
    stores = provinces_eci.get('stores')[0]

    cityname = stores.get('locality_name')
    storename = stores.get('name')
    print (storename)

    speech = "Shopping Centers with stock in " + cityname + " are: " + storename
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
    
