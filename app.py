from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)
from pymongo import MongoClient


client = MongoClient('mongodb+srv://nasha:rlar3986!!@cluster0.e9ccedb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
doc ={
    "id" : "c",
    "password": "c",
    "name" : "c",
    "index" : 3,
    "wishindex" : 1,
    "wish" : "모르는 사람 도와주기"
}
#content > div > div:nth-child(3) > div > div.row-masonry.search-results > div:nth-child(1) > div > div > div > a > img
#content > div > div:nth-child(3) > div > div.row-masonry.search-results > div:nth-child(2) > div > div > div > a > img
@app.route('/')
def home():
    #db.tree.insert_one(doc)
    return render_template('goTree.html')

@app.route('/tree', methods=["GET"])
def tree():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get("https://kr.freepik.com/free-photos-vectors/wish", headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    images = soup.find_all('img', attrs={'class': "min-size-to-snippet"})
    tt = soup.find('img', attrs={'class': 'min-size-to-snippet'})
    arrayimage = []
    for image in images:
        img = image['src']
        arrayimage.append(img)
    all_id = list(db.tree.find({}))
    for i in range(len(all_id)):
        all_id[i]['_id']=str(all_id[i]['_id'])
    return jsonify({"all_id" : all_id, "img" : arrayimage, "msg": "문제없다!"})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)