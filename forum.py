import os
import hashlib
from flask import Flask, render_template, request
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQL_ALCH_URL = "SQLALCHEMY_DATABASE_URI"

app.config[SQL_ALCH_URL] = "sqlite:///" + os.path.join(BASEDIR, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'

DB = SQLAlchemy(app)

class PostForm(FlaskForm):
    ''' 
        Post form to get data from the user
    '''
    textContent = StringField('Type your message here...', validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Post')

class Post(DB.Model):
    '''
        add models here
    '''
    __tablename__ = "posts"
    id = DB.Column(DB.Integer, primary_key=True)
    content = DB.Column(DB.String(64), unique=False, index=True)
    ipHash = DB.Column(DB.String(64), unique=False, index=True)

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

    postForm = PostForm()

    requestIp = request.remote_addr
    ip_hash=hashlib.sha224(bytes(str(requestIp),"utf-8" ) ).hexdigest()[-8:]
    
    if postForm.validate_on_submit():

        textContent = postForm.textContent.data 
        your_post = str(textContent[:128])
        
        if len(your_post) == 0:
            return render_template("error.html")
 
        # Hash their IP and take the last 8 characters
        
        new_post = Post(content=str(your_post),ipHash=ip_hash)

        DB.session.add(new_post)
        DB.session.commit()

    all_posts = Post.query.all() # Get all posts
    postedData = { "posted": request.method == 'POST',"allposts": reversed(all_posts) }  

    return render_template("index.html", post=postedData, form=postForm, myIp=ip_hash)

if __name__ == '__main__':
    app.run()