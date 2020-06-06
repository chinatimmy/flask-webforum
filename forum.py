'''
    Flask Web Forum! TxT Board
    Instructions are in the README.md
'''
import os
import hashlib
from time import strftime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
# UNUSED IMPORTS
# from markupsafe import escape
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from werkzeug.security import generate_password_hash, check_password_hash

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
    text_content = StringField('Type your message here...',
                               validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Post')

class Post(DB.Model):
    '''
        Declare and initialize database and variables
    '''
    __tablename__ = "posts"
    id = DB.Column(DB.Integer, primary_key=True)
    content = DB.Column(DB.String(64), unique=False, index=True)
    ipHash = DB.Column(DB.String(64), unique=False, index=True)
    timestamp = DB.Column(DB.String(64), unique=False, index=True)

DB.drop_all()
DB.create_all()

@app.route('/favicon.ico')
def favicon():
    '''
        Placeholder
    '''
    return ""

@app.route('/', methods=['GET', 'POST'])
def posts():
    '''
        Displays the landing page
    '''
    post_form = PostForm()
    request_ip = request.environ['HTTP_X_FORWARDED_FOR']
    ip_hash = hashlib.sha224(bytes(str(request_ip), "utf-8")).hexdigest()[-16:]
    sys_time = "%s" % strftime('%I:%M:%S %p')

    if post_form.validate_on_submit():
        text_content = post_form.text_content.data
        your_post = str(text_content[:128])
    
        if len(your_post) == 0:
            return render_template("error.html")
    
        # Hash their IP and take the last 8 characters
        new_post = Post(content=str(your_post), ipHash=ip_hash, timestamp=sys_time)
        # refresh database
        DB.session.add(new_post)
        DB.session.commit()
    
    all_posts = Post.query.all() # Get all posts
    posted_data = {"posted": request.method == 'POST', "allposts": reversed(all_posts)}
    
    return render_template("index.html", post=posted_data, form=post_form, myIp=ip_hash)

if __name__ == '__main__':
    app.run()
