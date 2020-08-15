from flask import Flask,render_template,request
from s1 import goods as task_goods
from s2 import callback

app = Flask(__name__)

goods_list = [
    {"id":1,"title":"手机"},
    {"id":2,"title":"电脑"},
    {"id":3,"title":"电视"}
]

@app.route("/")
def index():

    return render_template("index.html",goods=goods_list)

@app.route("/goods")
def goods():
    good_id = request.args.get("id")
    result = task_goods.delay(good_id)

    return render_template("goods.html",task_id=result.id)

@app.route("/res")
def res():
    task_id = request.args.get("task_id")
    result = callback(task_id)
    return render_template("res.html",msg=result)

if __name__ == '__main__':
    app.run()