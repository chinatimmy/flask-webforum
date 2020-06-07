from models import *
from forms import *

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
