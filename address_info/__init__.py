#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Results, Request, User, RequestError
from flask import session as login_session
import random
import string
import excel
import httplib2
import json
from flask import make_response
import requests
import pandas as pd
from tablib import Dataset
import numpy as np
import excel
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# importing the requests library
import requests


engine = create_engine('sqlite:///address_info.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



app = Flask(__name__)


@app.route('/home/<string:address>', methods=['GET'])
def getSheet(address):
    def filter_address(address):
        address_query = str(address.lower())
        return address_query
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    location = filter_address(address)
    appkey = "your_appid"
    PARAMS = {'address':location,'key':appkey}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    try:
        # create new successful request
        new_request = Request(user_input=address, request_status=data['status'], user_id=1)
        session.add(new_request)
        session.commit()
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        formatted_address = data['results'][0]['formatted_address']
        place_id = data['results'][0]['place_id']
        long_name = data['results'][0]['address_components'][0]['long_name']
        types = data['results'][0]['address_components'][0]['types'][0]
        new_result = Results(latitude=latitude, longitude=longitude, formatted_address=formatted_address,
        place_id=place_id,long_name=long_name,types=types,request_id=new_request.id)
        session.add(new_result)
        session.commit()
        return "Latitude:%s\nLongitude:%s\nFormatted Address:%s\nPlace Id:%s" %(latitude, longitude,formatted_address,place_id)
    except IndexError:
        new_request = Request(user_input=address, request_status=data['status'], user_id=1)
        session.add(new_request)
        session.commit()
        print('added new request With Problem.. creating new error recored..')
        newerror = RequestError(user_input=address, request_status=data['status'], error_message=data['error_message'],request_id=new_request.id,)
        session.add(newerror)
        session.commit()
        print('created Error recored..')
        return 'Sorry There Is a problem in request which is :<br /><br /> %s' %newerror.error_message
    return str(data)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080, threaded=False)
