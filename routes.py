from models import *
from forms import *
from logic import *

# Render the main screen
@app.route('/', methods=['GET', 'POST'])
def posts():
    '''
        Displays the landing page
    '''
    post_form = PostForm()
    request_ip = "test" # request.environ['HTTP_X_FORWARDED_FOR']

    # create an IP hash to ID users in our database
    ip_hash = hashlib.sha224(bytes(str(request_ip), "utf-8")).hexdigest()[-16:]
    sys_time = "%s" % strftime('%I:%M:%S %p')

    if post_form.validate_on_submit():
        
        text_content = post_form.text_content.data
        new_post = Post(content=str(text_content), ipHash=ip_hash, timestamp=sys_time)

        DB.session.add(new_post)
        DB.session.commit()
    
    all_posts = Post.query.all() # Get all posts
    
    # Delete the oldest post if post limit reached
    if len(all_posts) >= POST_LIMIT:
        DB.session.delete(all_posts[0])
        DB.session.commit()

    posted_data = {"posted": request.method == 'POST', "allposts": reversed(all_posts)}
    
    return render_template("index.html", post=posted_data, form=post_form, myIp=ip_hash)
