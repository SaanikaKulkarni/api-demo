# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 05:14:55 2020

@author: associate
"""

from flask import Flask, request, jsonify, render_template, url_for, redirect
import pymongo

app = Flask(__name__)
app.config["DEBUG"] = True

def create_mongo_session(database, collection):
    client = pymongo.MongoClient('localhost', 27017)
    db = client[database]
    col = db[collection]
    return db, col

def parse_form():
    x = {}
    d = request.form
    for key in d.keys():
        value = request.form.getlist(key)
        for val in value:
            x[key] = val
    return x

def mongo_find(query):
    _, col = create_mongo_session('saanika_practice', 'api_coll')
    find_result = []
    for i in col.find(query):
        find_result.append(i)
    return str(find_result)


def mongo_insert_one(doc):
    _, col = create_mongo_session('saanika_practice', 'api_coll')
    col.insert_one(doc)


def mongo_insert_many(doc):
    _, col = create_mongo_session('saanika_practice', 'api_coll')
    col.insert_many(doc)


@app.route("/", methods=["GET"])
def home_page():
    return render_template('index.html')

@app.route('/api/v1', methods=['GET'])
def api_root():
    return render_template('docs.html')

@app.route('/api/v1/mongo/find/all', methods=['GET'])
def api_mongo_find_all():
    return mongo_find({})


@app.route('/api/v1/mongo/find', methods=['GET', 'POST'])
def api_mongo_find():
    if request.method == 'GET':
        return render_template('query.html')
    elif request.method == 'POST':
        data = parse_form()
        return mongo_find(data)


@app.route('/api/v1/mongo/insert', methods=['GET', 'POST'])
def api_mongo_insert():
    if request.method == 'GET':
        return render_template('mongoinsert.html')
    elif request.method == 'POST':

        data = parse_form()
        
        mongo_insert_one(data)

        return redirect(url_for('api_root'))



app.run(port=35080)