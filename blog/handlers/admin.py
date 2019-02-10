from flask import Blueprint, render_template,redirect,url_for,request
from blog.forms import LoginForm
from blog.models import db,User,Category,Blog
from flask_login import login_user, logout_user,login_required
from flask import jsonify
from datetime import datetime 
import json

admin = Blueprint('admin', __name__,url_prefix='/admin')

@admin.route('/')
@login_required
def blog_manage():
    
    return render_template('admin/blog_manage.html')

@admin.route('/category_manage')
@login_required
def category_manage():
    return render_template('admin/category_manage.html')



@admin.route('/blog')
@login_required
def blogs():
    blog_list=[]
    for b in Blog.query.all():
        item={}
        item['id']=b.id
        item['title']=b.title
        item['category']=Category.query.filter_by(id=b.category_id).first().name
        item['isRecommand']=b.isRecommand
        item['status']=b.status
        # if b.isRecommand==1:
        #     item['isRecommand']= '是'
        # else:
        #     item['isRecommand']= '否'
        # if b.status==1:
        #     item['status']='已发布'
        # else:
        #     item['status']='草稿'
        item['created_at']= b.created_at.strftime("%Y-%m-%d %H:%M:%S") 
        item['updated_at']= b.updated_at.strftime("%Y-%m-%d %H:%M:%S") 
        blog_list.append(item)
    result={}
    result['total']=len(blog_list)
    result['rows'] = blog_list
    return json.dumps(result)

@admin.route('/category')
@login_required
def categories():
    category_list = category_list=[]
    # print(type(Category.query.all()))
    for c in Category.query.all():
        item = {}
        item['id']=c.id
        item['name']=c.name
        item['count']=len(c.blogs)
        item['created_at']= c.created_at.strftime("%Y-%m-%d %H:%M:%S") 
        item['updated_at']= c.updated_at.strftime("%Y-%m-%d %H:%M:%S") 
        category_list.append(item)
    result={}
    result['total']=len(category_list)
    result['rows'] = category_list
    return json.dumps(result)


@admin.route('/saveCategory', methods=['GET','POST'])
@login_required
def saveCategory():
    id = request.form.get('id',-1)
    name = request.form.get('name','其他').strip()
    if id != -1 and Category.query.filter_by(id=id).first():
        category = Category.query.filter_by(id=id).first()    
    else:
        category = Category()
    category.name= name
    Category.updated_at = datetime.now
    db.session.add(category)
    db.session.commit()
    return jsonify({"code":200})  

@admin.route('/getCategory')
@login_required
def getCategory():
    id = int(request.args.get('id','-1'))
    # print(id)
    category = Category.query.filter_by(id=id).first()
    result = {
        'name':category.name
    }
    return jsonify(result)

@admin.route('/deleteCategory', methods=['GET','POST'])
@login_required
def deleteCategory():
    idlist = request.form.get('idstr',[]).split('.')
    for id in idlist:
        category = Category.query.filter_by(id=int(id)).first()
        db.session.delete(category)
    db.session.commit()
    return jsonify({"code":200})  

@admin.route('/editBlog')
@login_required
def editBlog():
    categories = Category.query.all()
    blog = Blog()
    return render_template('admin/edit_blog.html',categories=categories,blog=blog)

@admin.route('/release', methods=['GET','POST'])
@login_required
def release():
    
    if request.form.get('id'):
         blog = Blog.query.filter_by(id=int(request.form.get('id'))).first()
    else:
        blog=Blog()
    blog.title = request.form.get('title')
    blog.category_id = int(request.form.get('category_id'))
    blog.isRecommand = request.form.get('isRecommand')
    blog.tags = request.form.get('tags')
    blog.info = request.form.get('info')
    blog.status = request.form.get('status')
    blog.content = request.form.get('content')

    db.session.add(blog)
    db.session.commit()
    return jsonify({"code":200})  

@admin.route('/getBlog/<id>')
@login_required
def getBlog(id):
    # id = int(request.args.get('id','-1'))
    categories = Category.query.all()
    print(id)
    # if id == -1:
    #     blog = Blog()
    # return render_template('admin/edit_blog.html',categories=categories)
    # else:
    blog = Blog.query.filter_by(id=id).first()
    print(blog.title)
    return render_template('admin/edit_blog.html',categories=categories,blog=blog)

@admin.route('/recall', methods=['GET','POST'])
@login_required
def recall():
    idlist = request.form.get('idstr',[]).split('.')
    for id in idlist:
        blog = Blog.query.filter_by(id=int(id)).first()
        blog.status=0
        db.session.add(blog)
    db.session.commit()
    return jsonify({"code":200})  

@admin.route('/deleteBlog', methods=['GET','POST'])
@login_required
def deleteBlog():
    idlist = request.form.get('idstr',[]).split('.')
    for id in idlist:
        blog = Blog.query.filter_by(id=int(id)).first()
        db.session.delete(blog)
    db.session.commit()
    return jsonify({"code":200})  

@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('front.login'))