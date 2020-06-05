'''
ToDo:
Break after Length
Set max Length
Remove Scollbars in iFrame
Fix SQLALCHEMY_TRACK_MODIFICATIONS error
Formatting support for certian markup with CSS
'''


import os
from flask import Flask
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
sql_alch_url = "SQLALCHEMY_DATABASE_URI"
app.config[sql_alch_url] = "sqlite:///" + os.path.join(basedir,'data.sqlite')
db = SQLAlchemy(app)

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
    return "<em>Append your message to the URL</em> <br>Your Post: <b> " + str(your_post) + """</b><iframe scrolling="yes" width="100%" height="95%" style="border:0px solid black;" src="/posts/" title="Posts"></iframe>"""

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
