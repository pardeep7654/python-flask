import os

from datetime import datetime
from fileinput import filename

from click import DateTime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request,session,redirect,url_for
import  json
from werkzeug.utils import redirect


with open('config.json','r') as f:
    params=json.load(f)["params"]

local_server=True

app = Flask(__name__)
app.secret_key="mundi"

app.config['UPLOAD_FOLDER']="static/uploads/"

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(35), nullable=False)
class Posts(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80),nullable=False)
    slug=db.Column(db.String(25),nullable=False)
    content=db.Column(db.String(500),nullable=False)
    tagline=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(12),nullable=False)
    img_file = db.Column(db.String(12), nullable=True)



@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:5]

    return render_template("index.html",params=params,posts=posts)


@app.route("/about")
def abt():
    return render_template("about.html",params=params)


@app.route("/post")
def smp():
    return render_template("post.html",params=params)


@app.route("/contact", methods=["GET", "POST"])
def ctck():
    if request.method == "POST":
        '''Add entry to database'''
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        # date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()

    return render_template("contact.html",params=params)


@app.route("/post/<string:post_slug>",methods=["GET","POST"])
def app_get(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post)

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if 'user' in session and session['user']==params["admin_user"]:
        posts=Posts.query.all()
        return render_template('dashboard.html',params=params,posts=posts)
    if request.method=='POST':
        # redirect to admin page
        username=request.form.get("uname")
        userpass=request.form.get("upass")
        if (userpass==params["admin_pass"] and username==params['admin_user']):
            #set the session variable
            session["user"]=username
            #fetch the posts
            posts=Posts.query.all()
            return render_template("dashboard.html",params=params,posts=posts)

    return render_template('login.html',params=params)



@app.route("/edit/<string:sno>",methods=['GET','POST'])
def editPost(sno):
    if 'user' in session and session['user']==params['admin_user']:
        if request.method=='POST':
            box_title=request.form.get('title')
            tline=request.form.get('tline')
            slug=request.form.get('slug')
            content=request.form.get('content')
            date=datetime.now()
            # CHECK IF post request has file
            if 'img_file' not in request.files:
                return  'No file part'
            file=request.files['img_file']
            if(file.filename==''):
                return 'No file Selected'
            if file:
                filename=file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                img_file=filename
            if(sno=='0'):
                post=Posts(title=box_title,slug=slug,content=content,tagline=tline,img_file=img_file,date=date)
                db.session.add(post)
                db.session.commit()
                return  redirect("/dashboard")
            else:
                post=Posts.query.filter_by(sno=sno).first()
                post.title=box_title
                post.slug=slug
                post.tagline=tline
                post.content=content
                post.date=date
                post.img_file=img_file
                db.session.commit()
                return  redirect("/dashboard")

        post=Posts.query.filter_by(sno=sno).first()
        return render_template("edit.html",sno=sno,post=post,params=params)


@app.route("/logout")
def lgtout():
    session.pop("user")
    return  redirect("/")
@app.route("/delete/<string:sno>",methods=['GET','POST'])
def delete(sno):
    if 'user' in session and session['user']==params['user_name']:
        post=Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return  redirect("/dashboard")
app.run(debug=True)
