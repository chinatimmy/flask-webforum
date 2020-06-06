'''
    To start the server, run these commands!
    touch data.sqlite
    export FLASK_APP=forum.py
    flask run
'''
import os
from flask import Flask, render_template, request
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQL_ALCH_URL = "SQLALCHEMY_DATABASE_URI"
app.config[SQL_ALCH_URL] = "sqlite:///" + os.path.join(BASEDIR, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
DB = SQLAlchemy(app)

class Post(DB.Model):
    '''
        add models here
    '''
    __tablename__ = "posts"
    id = DB.Column(DB.Integer, primary_key=True)
    content = DB.Column(DB.String(64), unique=False, index=True)

DB.drop_all()
DB.create_all()

@app.route('/favicon.ico')
def favicon():
    '''
        returns ""
    '''
    return ""

@app.route('/', methods=['GET', 'POST'])
def posts():
    '''
        display the landing page
    '''
    if request.method == 'POST':
        your_post = str(request.form['post'][:128])
        if len(your_post) == 0:
            return render_template("error.html")
        new_post = Post(content=str(your_post))
        DB.session.add(new_post)
        DB.session.commit()

    all_posts = Post.query.all()

    return render_template("index.html", post={
        "posted": request.method == 'POST',
        "allposts": reversed(all_posts)
    }     
)

if __name__ == '__main__':
    app.run()