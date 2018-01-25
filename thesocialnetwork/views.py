import os
import shutil
from strgen import StringGenerator
#  from Crypto.Cipher import AES
from cryptography.fernet import Fernet

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import signing
from notify.signals import notify

from .models import UserProfile, UserFriendShip, get_image_path
from .forms import UserInfoForm

#  obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
#  obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
key = Fernet.generate_key()
cipher_suite = Fernet(key)


def home(request):
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
            user = User.objects.get(id=request.user)
            user_profile = user.userprofile
            # user_info = UserProfile.objects.select_for_update().filter(user=request.user)
            user_profile.update(dob=form['dob'],
                            about=form['about'],
                    )
            # TODO use single update
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
                user_profile.update(image=filename)
                return HttpResponseRedirect(reverse('profile'))


def search_users(request, data):
    users = User.objects.filter(first_name__icontains=str(data)).exclude(id=int(request.user.id))
    # search_results = []
    # user_secret_info = []
    # user_image_location = []
    # for user in list_of_users:
        # # user_secret_info.append(signing.dumps({'user_data': user.id}))
        # search_results.append({'img': user.userprofile.image
        # user_image_location.append(img)

    # user_data = zip(list_of_users, user_secret_info, user_image_location)
    return render(request, 'thesocialnetwork/searched_user_list.html.haml', {'users': users})



def send_request(request, data):
    to_user_id = signing.loads(data)['user_data']
    to_user = User.objects.get(id=to_user_id)
    from_user_id = int(request.user.id)
    form_user = User.objects.get(id=from_user_id)
    random_text = str(StringGenerator("[\d\w]{16}").render())
    friend_request = UserFriendShip.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            identifier=random_text
            )
    friend_request.save()
    description_text = cipher_suite.encrypt(random_text)
    notify.send(request.user, recipient=User.objects.get(id=to_user_id), actor=request.user,
            verb='sent you a friend request', nf_type='followed_user',
            description=description_text)
    import ipdb; ipdb.set_trace()
