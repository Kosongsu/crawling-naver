import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False

popular10lists = [{'name' : '헤드셋'},
    {'name' : '면도기'},
    {'name' : '스피커'},
    {'name' : '에어팟 프로'},
    {'name' : '제습기'},
    {'name' : '마스크 스트랩'},
    {'name' : '닌텐도 스위치'},
    {'name' : '크록스'},
    {'name' : '원피스'},
    {'name' : '마스크'}]

@app.route('/', methods=['GET'])
def home():
    return "<h1>The First Flask</h1><p>Just get a response from Flask</p>"

@app.route('/getJSONlists', methods=['GET'])
def api_all():
    return jsonify(popular10lists)

app.run()