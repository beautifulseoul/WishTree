from flask import Flask, render_template, request, jsonify, redirect, url_for
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)
from pymongo import MongoClient

import certifi

ca = certifi.where()


SECRET_KEY = 'SPARTA'

import jwt

import datetime

import hashlib


client = MongoClient('mongodb+srv://test:sparta@cluster0.zn30x0c.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
doc ={
    "id" : "nasha430",
    "password": "1234",
    "name" : "c",
    "index" : 3,
    "wishindex" : 1,
    "wish" : "모르는 사람 도와주기"
}
@app.route('/')
def home():

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.wishtree.find_one({"id": payload['id']})

        return render_template('wish.html', nickname=user_info["nick"])

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return  redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')

#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.wishtree.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.wishtree.find_one({'id': id_receive, 'pw': pw_hash})
    print(result)
    # 여기까지 확인함 TTTT

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120)  # utc timezone기준으로 now
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])  # jwt.decode는 jwt페이지에서 보는 decode와 같음
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.wishtree.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

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


@app.route("/wish/done", methods=["POST"])
def wish_done():
    num_receive = request.form['num_give']
    db.wish.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '완료👍🏻👍🏻'})

@app.route('/tree', methods=["GET"])
def tree():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get("https://kr.freepik.com/free-photos-vectors/wish", headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')                                  #soup (data의 html 가져오기)
    images = soup.find_all('img', attrs={'class': "min-size-to-snippet"})           #전체 html 에서 class가 min-size-to-snippet인 전체로 이미지 가져오기 ->images는 한줄한줄, img태그, img태그, img태그 형태이다.

    # tt = soup.find('img', attrs={'class': 'min-size-to-snippet'})     # find는 태그 하나만 찾는다.
    arrayimage = []                                                     # image 값을 담을 배열
    for image in images:                                                # 반복문을 통해 images 를 image로 떼어낸다.
        img = image['src']                                              #img태그에서 src 속성을 불러온다.
        arrayimage.append(img)                                          #반복문 돌때마다 img를 배열에 담는다.
    all_id = list(db.tree.find({},{'_id': False}))                      #tree db에 있는 정보를 모두 가져와 all_id에 담는다.
    #for i in range(len(all_id)):                                        # range(숫자) : 0부터 숫자-1까지 배열화 시킨다. len(all_id) 배열 all_id의 길이
    #    all_id[i]['_id'] = str(all_id[i]['_id'])                        # i번째 all_id의 _id 값을 all_id i번째에 스트링화 시킨다.
    return jsonify({"all_id": all_id, "img": arrayimage})               # json화 시켜서 클라이언트로 보낸다.




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


@app.route("/goTree/get", methods=["GET"])
def set_temp():
    user_list = list(db.wishtree.find({}, {'_id': False}))
    return jsonify({'users':user_list})

@app.route('/<path>')
def get_path(path):
    return render_template(path + '.html')

@app.route('/wish/<id>')
def get_tree_path(id):

    return render_template('wish.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
