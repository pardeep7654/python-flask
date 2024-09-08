from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def hello():
    # return  "<h2>hello world</h2>"
    return render_template("index.html")
@app.route("/pardeep")
def pardeep():
    name2="pardeep Mundi"
    # return  "<h2>Hello Pardeep</h2>"
    return render_template("about.html",name=name2)
@app.route("/bootstrap")
def bootstrap():
    return render_template("bootstrap.html")
app.run(debug=True)
# print(app)
# print(type(app))