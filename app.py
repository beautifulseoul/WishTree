from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.zn30x0c.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('wish.html')


@app.route("/wish", methods=["POST"])
def wish_post():
    wish_receive = request.form['wish_give']
    doc = {
        'wish': wish_receive
    }

    db.wish.insert_one(doc)

    return jsonify({'msg': '소원등록🐰'})


@app.route("/wish", methods=["GET"])
def wish_get():
    wish_list = list(db.wish.find({}, {'_id': False}))
    return jsonify({'wish': wish_list})


# @app.route("/wish/done", methods=["POST"])
# def wish_done():
#     num_receive = request.form['num_give']
#     db.wish.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
#
#     return jsonify({'msg': '완료👍🏻👍🏻'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
