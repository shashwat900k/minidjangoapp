import os
import shutil
from datetime import datetime
import re

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import signing
from django.db.models import Q

from .models import UserProfile, UserFriendShip, UserPost, UserLike, get_image_path
from .forms import UserInfoForm

def home(request):
    if request.user.id:
        posts_by_friends = []
        post_reactions = []
        friends = UserFriendShip.objects.filter(Q(from_user=request.user) | Q(to_user=request.user)).filter(is_accepted=True)
        for row in friends:
            posts = UserPost.objects.filter(Q(user=row.from_user) | Q(user=row.to_user)).exclude(user=request.user)
            for post in posts:
                reactions = UserLike.objects.filter(content_id=post)
                post_reactions.append(reactions)
                post.id = signing.dumps({'id': post.id})
                posts_by_friends.append(post)
        data = zip(posts_by_friends, post_reactions)
        return render(request, 'thesocialnetwork/home.html.haml', {'data': data})
    else:
        return render(request, 'thesocialnetwork/home.html.haml')

def signup(request):
    return render(request, 'thesocialnetwork/signin.html.haml')


def profile(request, user_id=None):
    if user_id is None:
        user_id = request.user.id
    can_edit = (user_id == request.user.id)
    user = User.objects.get(id=user_id)
    profile = user.userprofile
    img = profile.image.name
    if img == '':
        img = None

    return render(request, 'thesocialnetwork/userprofile.html.haml', {'profile': profile, 'can_edit': can_edit, 'img': img})


def update_profile(request):
    if len(request.POST) == 0:
        return render(request, 'thesocialnetwork/updateprofile.html.haml')
    else:
        form = UserInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.cleaned_data
            user = User.objects.get(id=request.user.id)
            user_profile = user.userprofile
            user_profile.dob=form['dob']
            user_profile.about=form['about']
            if 'image' in request.FILES.keys():
                # TODO this profile_pic path to settings only till photos
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media', 'photos', str(request.user.id))
                if os.path.exists(path):
                    shutil.rmtree(path)
                myfile = request.FILES['image']
                filename = myfile.name
                location = get_image_path(request.user, myfile.name)
                fs = FileSystemStorage()
                filename = fs.save(location, myfile)
                user_profile.image=filename
            user_profile.save()
            return HttpResponseRedirect(reverse('profile'))


def search(request, data):
    users = User.objects.filter(first_name__icontains=str(data)).exclude(id=int(request.user.id))
    is_friend_request_already_sent = []
    for user in users:
        request_status = UserFriendShip.objects.filter((Q(from_user=request.user) & Q(to_user=user)) |
                (Q(from_user=user) & Q(to_user=request.user))).first()
        if request_status is None:
            is_friend_request_already_sent.append(False)
        else:
            is_friend_request_already_sent.append(request_status)
    user_data = zip(users, is_friend_request_already_sent)
    return render(request, 'thesocialnetwork/searched_user_list.html.haml', {'users': user_data, 'user': request.user})


def show_notifications(request):
    all_friend_requests = UserFriendShip.objects.filter((Q(to_user=request.user) & Q(is_pending=True)) | (Q(from_user=request.user) & Q(is_accepted=True)))
    user_posts = UserPost.objects.filter(user=request.user)
    #  import ipdb; ipdb.set_trace()
    user_reactions = []
    for post in user_posts:
        reactions = UserLike.objects.filter(content_id=post)
        for reaction in reactions:
            user_reactions.append(reaction)
    return render(request, 'thesocialnetwork/show_notifications.html.haml', {'all_friend_requests': all_friend_requests,
            'user_reaction': user_reactions})


def accept_request(request, request_id):
    friend_request = UserFriendShip.objects.filter(id=int(request_id)).first()
    friend_request.is_accepted = True
    friend_request.is_pending = False
    friend_request.save()
    return HttpResponseRedirect(reverse('show_notifications'))

def reject_request(request, request_id):
    friend_request = UserFriendShip.objects.filter(id=int(request_id)).first()
    friend_request.is_accepted = False
    friend_request.is_pending = False
    friend_request.save()
    return HttpResponseRedirect(reverse('show_notifications'))

def send_request(request, user_id):
    to_user = User.objects.get(id=int(user_id))
    from_user = User.objects.get(id=int(request.user.id))
    check_if_request_already_sent = UserFriendShip.objects.filter(from_user=from_user, to_user=to_user).first()
    if check_if_request_already_sent is None:
        check_if_request_already_sent = UserFriendShip.objects.filter(from_user=to_user, to_user=from_user).first()
    if check_if_request_already_sent is None:
        friend_request = UserFriendShip.objects.create(
                from_user=from_user,
                to_user=to_user,
                time_of_request=datetime.now()
                )
        friend_request.save()
    return HttpResponseRedirect(reverse('profile'))


def write_something(request):
    if len(request.POST) == 0:
        return render(request, 'thesocialnetwork/write_something.html.haml')
    else:
        content = str(request.POST['content'])
        content = re.sub('[!#$@=+]','',content)
        user_post = UserPost(
                user = request.user,
                text_content = content,
                created_at = datetime.now()
                )
        user_post.save()
        return HttpResponseRedirect(reverse('profile'))


def user_reaction(request, data):
    value=signing.loads(data)
    id = int(value['id'])
    post = UserPost.objects.get(id=id)
    if_already_liked = UserLike.objects.filter(liked_by_user=request.user, content_id=post)
    if not if_already_liked:
        user_like = UserLike(
            liked_by_user = request.user,
            content_id = post
        )
        user_like.save()
    else:
        if_already_liked.delete()
    return HttpResponseRedirect(reverse('home'))


def show_friends(request):
    friend_list = []
    friends = UserFriendShip.objects.filter(Q(is_accepted=True) &
            (Q(from_user=request.user) | Q(to_user=request.user)))
    for friend in friends:
        if friend.from_user == request.user:
            friend_list.append(friend.to_user)
        else:
            friend_list.append(friend.from_user)
    return render(request, 'thesocialnetwork/show_friends.html.haml', {'friend_list': friend_list})

def user_content(request):
    data = None
    post_reactions = []
    posts_by_friends = []
    posts = UserPost.objects.filter(user=request.user)
    if posts:
        for post in posts:
            reactions = UserLike.objects.filter(content_id=post)
            post_reactions.append(reactions)
            post.id = signing.dumps({'id': post.id})
            posts_by_friends.append(post)
        data = zip(posts_by_friends, post_reactions)
    return render(request, 'thesocialnetwork/user_content.html.haml', {'user_content': data})
