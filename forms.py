from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
# UNUSED IMPORTS
# from markupsafe import escape
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from werkzeug.security import generate_password_hash, check_password_hash

class PostForm(FlaskForm):
    '''
        Post form to get data from the user
    '''
    text_content = StringField('Type your message here...',
                               validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Post')