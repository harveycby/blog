from flask import Blueprint, render_template,request,redirect,url_for
from blog.models import db,Category,Blog,User
from blog.forms import LoginForm
from flask_login import login_user

front = Blueprint('front', __name__)

@front.route('/')
def index():
    blogs = Blog.query.filter_by(status=1).order_by(Blog.created_at.desc()).limit(5)
    page = request.args.get('page',default=1,type=int)
    pagination = Blog.query.paginate(
        page=page,
        per_page=3,
        error_out=False
    )
    return render_template('home.html', pagination=pagination,blogs=blogs)

@front.route('/detail/<int:id>')
def blogDetail(id):
    blog = Blog.query.filter_by(id=id).first()
    return render_template('detail.html', blog=blog)


@front.route('/categories')
def categories():
    categories = Category.query.all()
    for category in categories:
        if len(category.blogs)<=0:
            categories.remove(category)
    page = request.args.get('page',default=1,type=int)
    category = Category.query.filter_by(id=categories[0].id).first()
    pagination = Blog.query.filter_by(category_id=categories[0].id).paginate(
        page=page,
        per_page=5,
        error_out=False
    )
    return render_template('categories.html',categories=categories,pagination=pagination,category=category)

@front.route('/classify/<int:id>')
def category_classify(id):
    categories = Category.query.all()
    category = Category.query.filter_by(id=id).first()
    print(category.name)
    for c in categories:
        if len(c.blogs)<=0:
            categories.remove(c)
    page = request.args.get('page',default=1,type=int)
    pagination = Blog.query.filter_by(category_id=id).paginate(
        page=page,
        per_page=5,
        error_out=False
    )
    return render_template('categories.html',categories=categories,pagination=pagination,category=category)

@front.route('/archive')
def archive():
    blogs = Blog.query.all()
    # month_field = extract('month', Blog.created_at)
    # year_field = extract('year', Blog.created_at)
    blog_dict={}
    year_set=set()
    for blog in blogs:
        year_set.add(blog.created_at.strftime('%Y-%m'))
    for year in year_set:
        blog_dict[year]={}
    for blog in blogs:
        if blog.created_at.strftime('%Y-%m') in blog_dict.keys():
            blog_dict[blog.created_at.strftime('%Y-%m')][blog.created_at.strftime('%m-%d')]=[]
    for blog in blogs:
        if blog.created_at.strftime('%Y-%m') in blog_dict.keys():
            blog_dict[blog.created_at.strftime('%Y-%m')][blog.created_at.strftime('%m-%d')].append(blog)
    print(blog_dict)
    

    return render_template('archive.html',blogs=blogs,blog_dict= blog_dict)

@front.route('/about')
def about():
    
    return render_template('about.html')

@front.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(url_for('admin.blog_manage'))
    else:
        return render_template('login.html',form=form)