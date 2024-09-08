from flask import  Flask,render_template

app=Flask(__name__)

# @app.route("/home")
# def home():
#     return render_template("index.html")

@app.route("/")
def home():
    name="navneet"
    return render_template("index.html",username=name)
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/post")
def samplePost():
    return render_template("post.html")

@app.route("/contact")
def contact():
    return  render_template("contact.html")

app.run(debug=True)