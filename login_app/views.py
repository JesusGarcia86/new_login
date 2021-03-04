from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import UserManager, User, MessageManager, MessagePost, Comment

def home_reroute(request):
    return redirect('/login')

def login(request):
    return render(request, "login.html")

def register(request):
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/login')

        user_pw=request.POST['pw']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/wall')
    return redirect('/login')

def log_in(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/wall')
            else:
                messages.error(request, "Password was incorrect.")
        else:
            messages.error(request, "Email was not found.")
    return redirect('/login')

def  sucess(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        'all_messages':MessagePost.objects.all()
    }
    return render(request, "wall.html", context)

def create_mess(request):
    if request.method=='POST':
        print(request.POST)
        error=MessagePost.objects.empty_validator(request.POST)
        if error:
            messages.error(request, error)
            return redirect('/wall')
        MessagePost.objects.create(content=request.POST['contents'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/wall')
    return redirect('/login')

def create_comm(request):
    if request.method=='POST':
        Comment.objects.create(comment=request.POST['contents'], poster=User.objects.get(id=request.session['user_id']), message=MessagePost.objects.get(id=request.POST['message']))
        return redirect('/wall')
    return redirect('/login')

def logout(request):
    print(request.session)
    request.session.flush()
    print(request.session)
    return redirect('/login')

def profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'profile.html', context)

def delete_mess(request, mess_id):
    MessagePost.objects.get(id=mess_id).delete()
    return redirect('/wall')

def delete_comm(request, comm_id):
    Comment.objects.get(id=comm_id).delete()
    return redirect('/wall')

def add_like(request, user_id):
    liked_message = MessagePost.objects.filter(id=user_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    print(user_liking.first_name)
    return redirect('/wall')

def edit(request, user_id):
    context = {
        'edit':User.objects.get(id=user_id)
    }
    return render(request, 'edit.html', context)

def update(request, user_id):
    edit_user = User.objects.get(id=user_id)
    edit_user.first_name = request.POST['f_n']
    edit_user.last_name = request.POST['l_n']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/wall')
