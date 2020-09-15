#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template, request, session,redirect,url_for
from models.models import PaperContent, User
from models.database import db_session
from datetime import datetime
from app import key
from hashlib import sha256
from app.scraper import url2list

#Flaskオブジェクトの生成
app = Flask(__name__)
app.secret_key = key.SECRET_KEY

@app.route("/")
@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"]
        all_contents = PaperContent.query.all()
        return render_template("index.html",name=name,all_contents=all_contents)
    else:
        return redirect(url_for("top"))

@app.route("/url",methods=["post"])
def url():
    url = request.form["url"]
    print(url)
    title_en, abst_en_ls, title_jp, abst_jp_ls = url2list(url)
    print("英語タイトル：", title_en, "英語アブスト:", abst_en_ls,
     "日本語タイトル:", title_jp, "日本語アブスト:", abst_jp_ls)
    ### 課題、解決法、応用を初期化
    prob, sol, app = 0, 0, 0 

    ### DBにデータ保存
    #contents = [PaperContent(url,title_en,abst_en_ls[i],
    #title_jp,abst_jp_ls[i],prob,sol,app,datetime.now()) for i in len(abst_en_ls)]
    #contents = [PaperContent(url,title_en,abst_en_ls[i],
    #title_jp,abst_jp_ls[i],prob,sol,app,datetime.now()) for i in len(abst_en_ls)]
    abst_en = abst_en_ls
    abst_jp = abst_jp_ls
    db_session.add_all([
        PaperContent(url,title_en,abst_en[0],title_jp,abst_jp[0],
        prob,sol,app,datetime.now()),
        PaperContent(url,title_en,abst_en[1],title_jp,abst_jp[1],
        prob,sol,app,datetime.now()),
        PaperContent(url,title_en,abst_en[2],title_jp,abst_jp[2],
        prob,sol,app,datetime.now()),
    ])
    db_session.commit()

    """ title = request.form["title"]
    body = request.form["body"]
    content = PaperContent(title,body,datetime.now())
    db_session.add(content)
    db_session.commit() """

    return redirect(url_for("index"))

@app.route("/update",methods=["post"])
def update():
    content = PaperContent.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = PaperContent.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/login",methods=["post"])
def login():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top",status="wrong_password"))
    else:
        return redirect(url_for("top",status="user_notfound"))

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top",status="logout"))

@app.route("/registar",methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("newcomer",status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)


@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)

#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    app.run(debug=True)