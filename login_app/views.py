from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def create_user(request):
    if request.method == 'POST' :
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user=User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
            )
            print('You created a User')
            request.session['user_id'] = new_user.id
            request.session['first_name'] = new_user.first_name
            request.session['last_name'] = new_user.last_name
            request.session['email'] = new_user.email
            return redirect('/success')

def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, "This email has not yet been registered")
        return redirect('/')
    if  bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['email'] = user.email
        return redirect('/wall')
    else:
        messages.error(request, "Password does not match account")
        return redirect('/')
                
def success(request):
    return render(request, "success.html")

def wall(request):
    context = {
        "all_posts" : Post.objects.all(),
        "all_comments" : Comment.objects.all()
    }
    return render(request, "wall.html", context)

def post(request):
    if request.method == 'POST' :
        errors = Post.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wall')
        else:
            new_post=Post.objects.create(
                post_content=request.POST['post_content'],
                user=User.objects.get(id=request.session['user_id']),
            )
            print('You created a Post')
            return redirect('/wall')

def delete_post(request, post_id):
    post_to_delete=Post.objects.get(id=post_id)
    post_to_delete.delete()
    return redirect('/wall')

def comment(request):
    if request.method == 'POST' :
        errors = Comment.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wall')
        else:
            new_comment=Comment.objects.create(
                comment_content=request.POST['comment_content'],
                user=User.objects.get(id=request.session['user_id']),
                post=Post.objects.get(id=request.POST['post_id']),
            )
            print('You created a comment')
            return redirect('/wall')

def delete_comment(request, comment_id):
    comment_to_delete=Comment.objects.get(id=comment_id)
    comment_to_delete.delete()
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')