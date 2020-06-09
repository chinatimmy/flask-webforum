# UNUSED IMPORTS
# from markupsafe import escape
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from werkzeug.security import generate_password_hash, check_password_hash
import os
import hashlib
import random
import uuid; uuid.uuid4().hex.upper()[0:6]
from time import strftime, sleep
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from werkzeug.utils import secure_filename

'''
  _____       _ _
 |_   _|     (_) |
   | |  _ __  _| |_
   | | | '_ \| | __|
  _| |_| | | | | |_
 |_____|_| |_|_|\__|
'''
app = Flask(__name__)
rand1 = str(uuid.uuid4())
rand2 = str(uuid.uuid4())
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQL_ALCH_URL = "SQLALCHEMY_DATABASE_URI"
app.config[SQL_ALCH_URL] = "sqlite:///" + os.path.join(BASEDIR, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = "/uploads"
DB = SQLAlchemy(app)

# Limit how many posts are stored in the database
POST_LIMIT = 6969


'''
  ______
 |  ____|
 | |__ ___  _ __ _ __ ___
 |  __/ _ \| '__| '_ ` _ \
 | | | (_) | |  | | | | | |
 |_|  \___/|_|  |_| |_| |_|
'''


class PostForm(FlaskForm):
    '''
        Post form to get data from the user
    '''
    text_content = TextAreaField(
        'Type your message here...', validators=[
            DataRequired(), Length(
                min=1, max=150)])
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


'''
  _    ___   __  _    _ _____
 | |  | \ \ / / | |  | |_   _|
 | |  | |\ V /  | |  | | | |
 | |  | | > <   | |  | | | |
 | |__| |/ . \  | |__| |_| |_
  \____//_/ \_\  \____/|_____|
'''

'''
-START ANTI BOT-
'''
@app.route('/', methods=['GET'])
def null():
    codes = random.choice([307, 303])
    riteroute = random.choice(['null', 'land1', 'land2'])
    sleepytime = random.choice([.5,.2,.3])
    sleep(sleepytime)
    return redirect(url_for(riteroute), code=codes)

@app.route('/ping/' + rand2, methods=['GET'])
def land1():
    codes = random.choice([307, 303])
    riteroute = random.choice(['posts', 'null', 'land2'])
    sleepytime = random.choice([.1,.2,.3])
    sleep(sleepytime)
    return redirect(url_for(riteroute), code=codes)

@app.route('/pong/' + rand2, methods=['GET'])
def land2():
    codes = random.choice([307, 303])
    riteroute = random.choice(['posts', 'null', 'land1'])
    sleepytime = random.choice([.6,.9,.4])
    sleep(sleepytime)
    return redirect(url_for(riteroute), code=codes)

'''
-END ANTI BOT-
'''
@app.route('/post/' + rand1, methods=['GET', 'POST'])
def posts():
    '''
        Displays the landing page
    '''
    post_form = PostForm()
    request_ip = "test"  # request.environ['HTTP_X_FORWARDED_FOR']

    # create an IP hash to ID users in our database
    ip_hash = hashlib.sha224(bytes(str(request_ip), "utf-8")).hexdigest()[-16:]
    sys_time = "%s" % strftime('%I:%M:%S %p')

    if post_form.validate_on_submit():

        text_content = post_form.text_content.data
        new_post = Post(
            content=str(text_content),
            ipHash=ip_hash,
            timestamp=sys_time)

        DB.session.add(new_post)
        DB.session.commit()

    all_posts = Post.query.all()  # Get all posts

    # Delete the oldest post if post limit reached
    if len(all_posts) >= POST_LIMIT:
        DB.session.delete(all_posts[0])
        DB.session.commit()

    posted_data = {
        "posted": request.method == 'POST',
        "allposts": reversed(all_posts)}

    return render_template(
        ["land.html", "posts.html"],
        post=posted_data,
        form=post_form,
        myIp=ip_hash)


'''
  _                 _____      _   _   _ _
 | |               / ____|    | | | | (_) |
 | |     ___ ____ | |  __  ___| |_| |_ _| |_
 | |    / _ \_  / | | |_ |/ _ \ __| __| | __|
 | |___|  __// /  | |__| |  __/ |_| |_| | |_
 |______\___/___|  \_____|\___|\__|\__|_|\__|
'''

if __name__ == '__main__':
    app.run()
    DB.drop_all()
    DB.create_all()
