from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from content.models import Video, Like, Comment, Subscribe, Detail, Reply
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
import requests


url = 'http://localhost:8000/'

def home_page(request, *args, **kwargs):

    videos = requests.get(url+'video/').json()
    logged_user = None
    videos_detail = []

    for video in videos:
        vid = {**video, 'uploaded_by': requests.get(url+'user_by_id/'+str(video['uploaded_by_id'])).json()}
        videos_detail.append(vid)
    if request.COOKIES.get('auth'):
        logged_user = requests.get(url+'user/', headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()

    return render(request, 'home.html', {'videos': videos_detail, 'logged_user': logged_user})


def signup_page(request, *args, **kwargs):

    if (request.POST):
        response = requests.post(url+"signup/", json={
            'username': request.POST['name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name']
        })

        if(response.json() == 'fail'):
            return render(request, 'signup.html', {'error': 'user with this username already exists!!'})
        else :
            return redirect(home_page)
    else:
        return render(request, 'signup.html')

def login_page(request, *args, **kwargs):
    if (request.POST):

        token = requests.post(url+"login/", data = {'username': request.POST['name'], 'password': request.POST['password']}).json()


        if token != "fail":
            response = redirect(home_page)
            response.set_cookie("auth", token, expires=datetime.now()+timedelta(days=7), httponly=True)
            return response
        else:
            return render(request, 'login.html', {'error': 'invalid username or password!!'})
    else:
        return render(request, 'login.html')

def create_page(request, *args, **kwargs):
    if request.method == 'POST':
        requests.post(url+'video/', json={
            'url': FileSystemStorage().url(FileSystemStorage().save(request.FILES['filename'].name, request.FILES['filename'])),
            'title': request.POST['title'],
            'description': request.POST['desc']
        }, headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"})

        return redirect(home_page)

    else:
        if request.COOKIES.get('auth'):
            logged_user = requests.get(url+'user/', headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"})
            if logged_user:
                return render(request, 'create.html')
            return redirect(login_page)
        else:
            return redirect(login_page)

def update_page(request, *args, **kwargs):

    if request.method == 'POST':
        profile_pic = None
        profile_cover = None
        user_desc = None
        user = requests.get(url+'user/', headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()

        if (request.FILES.get('profile_pic') is not None):
            profile_pic = FileSystemStorage().url(FileSystemStorage().save(request.FILES['profile_pic'].name, request.FILES['profile_pic']))
        if (request.FILES.get('profile_cover') is not None):
            profile_cover = FileSystemStorage().url(FileSystemStorage().save(request.FILES['profile_cover'].name, request.FILES['profile_cover']))
        if (request.POST.get('user_desc') is not None):
            user_desc = request.POST['user_desc']

        print(requests.post(url+'user/', json={
            'profile_pic': profile_pic,
            'profile_cover': profile_cover,
            'user_description': user_desc,
            'username': user['username']
        }).json())

        return redirect('/user?uname='+user['username'])
    else:
        return render(request, 'update.html')

def video_page(request, *args, **kwargs):

    id = request.GET.get('id')
    video = requests.get(url+'video/'+id).json()
    video_detail = {**video, 'uploaded_by': requests.get(url+'user_by_id/'+str(video['uploaded_by_id'])).json()}
    videos = requests.get(url+'video/').json()
    videos_detail = []
    for video in videos:
        vid = {**video, 'uploaded_by': requests.get(url+'user_by_id/'+str(video['uploaded_by_id'])).json()}
        videos_detail.append(vid)
    logged_user = None
    likes = requests.get(url+'likes/'+id).json()
    comments = requests.get(url+'comments/'+id).json()
    comments_detail = []
    for comment in comments:
        comm = {**comment, 'commented_by': requests.get(url+'user_by_id/'+str(comment['commented_by_id'])).json()}
        comments_detail.append(comm)
    subscribers = requests.get(url+'subscribers/'+str(video['uploaded_by_id'])).json()
    like = False
    subscribe = False

    if request.COOKIES.get('auth'):
        logged_user = requests.get(url+'user/', headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()
        like = requests.get(url+'like/'+id, headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()
        subscribe = requests.get(url+'subscriber/'+str(video['uploaded_by_id']), headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()

    return render(request, 'video.html', {'video': video_detail, 'videos_data': videos_detail, 'liked': like, 'subscribed': subscribe, 'comments_data': comments_detail, 'likes_count': likes, 'subscribers_count': subscribers, 'logged_user': logged_user})


def user_page(request, *args, **kwargs):

    user = requests.get(url+'user/'+request.GET.get('uname')).json()
    logged_user = None
    subscribers = requests.get(url+'subscribers/'+str(user['id'])).json()
    subscribe = False

    if request.COOKIES.get('auth'):
        logged_user = requests.get(url+'user/', headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()
        subscribe = requests.get(url+'subscriber/'+str(user['id']), headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()


    return render(request, 'user.html', {'subscribers_count': subscribers, 'curr_user': user, 'subscribed': subscribe, 'logged_user': logged_user, 'videos_count': len(user['videos'])})


def logout_view(request, *args, **kwargs):
    response = redirect(home_page)
    response.delete_cookie("auth")
    return response


def like_view(request, *args, **kwargs):
    if request.COOKIES.get('auth'):
        logged_user = requests.get(url+'user/', headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()
        if logged_user:
            print(requests.post(url+'like/'+request.GET.get('video'), headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json())
            return redirect(f"/video?id={request.GET.get('video')}")
        else:
            return redirect(login_page)
    else:
        return redirect(login_page)


def comment_view(request, *args, **kwargs):

    if request.COOKIES.get('auth'):
        logged_user = requests.get(url+'user/', headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()
        if logged_user:
            requests.post(url+'comment/'+request.GET.get('id'), json={'content': request.POST.get('comment')}, headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"})
            return redirect(f"/video?id={request.GET.get('id')}")
        else:
            return redirect(login_page)
    else:
        return redirect(login_page)


def subscribe_view(request, *args, **kwargs):

    if request.COOKIES.get('auth'):
        logged_user = requests.get(url+'user/', headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json()
        if logged_user:
            print(requests.post(url+'subscriber/'+request.GET.get('subscribee'), headers={"authorization": f"Bearer {request.COOKIES.get('auth')}"}).json())

            if (request.GET.get('video') is not None):
                return redirect(f"/video?id={request.GET.get('video')}")
            else:
                return redirect(f"/user?uname={request.GET.get('uname')}")
        else:
            return redirect(login_page)
    else:
        return redirect(login_page)
