'''
ToDo:
Break after Length
Set max Length
Remove Scollbars in iFrame
Fix SQLALCHEMY_TRACK_MODIFICATIONS error
Formatting support for certian markup with CSS
Support image posting
'''


import os
from flask import Flask, render_template
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
sql_alch_url = "SQLALCHEMY_DATABASE_URI"
app.config[sql_alch_url] = "sqlite:///" + os.path.join(basedir,'data.sqlite')
db = SQLAlchemy(app)

# Add Models here
class Post(db.Model):
    __tablename__ = "posts"
    id=db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(64), unique=False, index=True)


db.drop_all()
db.create_all()

@app.route('/favicon.ico')
def favicon():
    return ""

@app.route('/')
def landing():
    return "<em>Append your message to the URL</em>"

@app.route('/<your_post>')
def index(your_post):
    your_post = str(your_post[:128])
    newPost = Post(content=escape(your_post))
    db.session.add(newPost)
    db.session.commit()
    return render_template("index.html", post={"data":your_post})



@app.route('/posts/')
def showAll():
    allPosts = Post.query.all()
    text = ""
    for post in reversed(allPosts):
        print(post.content)
        text = text + str(post.content) + "<br/>"
    return(text)

if __name__ == '__main__':
    app.run()


'''
to start the server run these commands
export FLASK_APP=Gaynigger.py
flask run
'''
