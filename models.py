from config import *
'''
    Models below
'''



class Post(DB.Model):
    '''
        Declare and initialize database and variables
    '''
    __tablename__ = "posts"
    id = DB.Column(DB.Integer, primary_key=True)
    content = DB.Column(DB.String(64), unique=False, index=True)
    ipHash = DB.Column(DB.String(64), unique=False, index=True)
    timestamp = DB.Column(DB.String(64), unique=False, index=True)
