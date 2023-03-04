from django.shortcuts import render
from .models import Chat,Group
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
# Create your views here.
@csrf_protect
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('/')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('/')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('/')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('/')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('/')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
       
       
        
        return redirect('/')
    return render(request,'signup.html')

@csrf_protect
def signin(request):
    if request.method == 'POST':
        print("hiiii")
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            print("account created")
            login(request, user)
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('/chat')
        else:
            print("account not created")
            messages.error(request, "Bad Credentials!!")
            return redirect('/')
    
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('/')

@login_required
def chat(request):
    if request.method=="POST":
        group_name=request.POST.get('text')
        group_in_db=Group.objects.filter(name=group_name).first()
        chats=[]
        if group_in_db:
            chats=Chat.objects.filter(group=group_in_db)
        
        else:
            g=Group(name=group_name)
            g.save()
            #print("group created")
        return render(request,'index.html',{'text':group_name,'chats':chats})
    return render(request,'index.html')