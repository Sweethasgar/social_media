from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import *
from itertools import chain
import random
# Create your views here.


@login_required(login_url='register')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    # following feeds
    user_following_list=[]
    feed=[]
    user_following=FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for username in user_following_list:
        feed_lists=Post.objects.filter(user=username).order_by('-image')
        feed.append(feed_lists)

    feed_list=list(chain(*feed))  

    # user suggestion
    all_user=User.objects.all()
    user_following_all=[]

    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)
    suggestion_list=[x for x in list(all_user) if (x not in list(user_following_all))]
    current_user=User.objects.filter(username=request.user.username)
    final_suggestion=[x for x in list(suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestion)

    username_list=[]
    user_profile_list=[]

    for users in final_suggestion:
        username_list.append(users.id)

    for idss in username_list:
        profile_list=Profile.objects.filter(id_user=idss)
        user_profile_list.append(profile_list)

    suggestion_list_profile=list(chain(*user_profile_list))    
   
    return render(request, 'index.html',{'user_profile':user_profile,'posts':feed_list,'suggestion_list_profile':suggestion_list_profile [:4]})


@login_required(login_url='register')
def search(request):
    user=User.objects.get(username=request.user.username)
    profile_object=Profile.objects.get(user=user)

    if request.method == 'POST':
        username=request.POST["username"]
        username_object=User.objects.filter(username__icontains=username)

        username_profile=[]
        username_profile_list=[]
        
        for users in username_object:
            username_profile.append(users.id)

        for idss in username_profile:
            profile_list=Profile.objects.filter(id_user=idss)
            username_profile_list.append(profile_list)     

        username_profile_list=list(chain(*username_profile_list))
    return render(request,'search.html',{'profile_object':profile_object,'username_profile_list':username_profile_list})

@login_required(login_url='register')
def upload(request):

    if request.method =='POST':
        user=request.user.username
        image=request.FILES.get("image_upload")    
        caption=request.POST["caption"]

        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save( )
        return redirect("/")
    else:
        return redirect("/")    
@login_required(login_url='register')
def liked(request):
    Username=request.user.username
    post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)

    liked_filter=LikedPost.objects.filter(username=Username,post_id=post_id).first()
    if liked_filter==None:
        new_like=LikedPost.objects.create(post_id=post_id,username=Username)
        new_like.save()
        post.likes=post.likes+1
        post.save()
        return redirect("/")
    else:
        liked_filter.delete()
        post.likes=post.likes-1
        post.save
        return redirect("/")


@login_required(login_url='register')
def profileView(request,pk):
    user_object=User.objects.get(username=pk)
    profile_object=Profile.objects.get(user=user_object)
    user_post=Post.objects.filter(user=pk) 
    user_post_len=len(user_post)

    follower=request.user.username
    user=pk

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text='unfollow'
    else:
        button_text='follow'    
    
    user_follower=len(FollowersCount.objects.filter(user=pk))
    user_following=len(FollowersCount.objects.filter(follower=pk))


    context={
        "user_object":user_object,
        "profile_object":profile_object,
        "user_post":user_post,
        "user_post_len":user_post_len,
        "button_text":button_text,
        "user_follower":user_follower,
        "user_following":user_following

    }
    return render(request, 'profile.html',  context)

@login_required(login_url='register')
def Follow(request):

    if request.method =="POST":
        follower=request.POST['follower']
        user=request.POST['user']

        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect("/profile/"+user)
        else:
            follower_add=FollowersCount.objects.create(follower=follower,user=user)
            follower_add.save()
            return redirect("/profile/"+user)    
    
    else:
        return redirect("/")


def Register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # email=form.cleaned_data["email"]
        if form.is_valid():
            # if User.objects.filter(email=email).exists():
            #     message="email is taken"
            #     return redirect('register')
            # else:
            user = form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password")
            login(request, user)
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(
                user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('index')

    context = {'form': form}
    return render(request, 'signup.html', context)


@login_required(login_url='register')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method=='POST':
        if request.FILES.get('image')==None:
            image=user_profile.profile_img
            bio=request.POST['bio']
            location=request.POST['location']
            user_profile.profile_img=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        if request.FILES.get('image') !=None:
            image=request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profile_img=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect('settings')    




    return render(request, "setting.html", {'user_profile': user_profile})    


def Login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                messages.success(request, message)
                return redirect('index')

            else:
                message = "login error your password or username does not match"
                messages.error(request, message)
    return render(request, "signin.html", context={'form': form})


@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')
