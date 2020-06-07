from routes import * 

'''
    Flask Web Forum! TxT Board
    Instructions are in the README.md
'''

DB.drop_all()
DB.create_all()
if __name__ == '__main__':
    app.run()
