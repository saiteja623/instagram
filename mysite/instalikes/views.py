from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import auth, User
from .models import likedby, userProfile, customUser, FriendRequest, post
from mysite import settings
from django.contrib.auth.decorators import login_required
import json

# Create your views here.1


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session["user1"] = username
            return redirect("homePage")

        else:
            return render(request, "registertodo.html")
    else:
        if request.session.has_key("user1"):
            return redirect("homePage")
        else:
            return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        passw = request.POST["password"]
        passw1 = request.POST["password1"]
        email = request.POST["email"]
        if passw == passw1:
            if User.objects.filter(username=username).exists():
                return render(request, "registertodo.html")
            else:
                user1 = User.objects.create_user(
                    username=username, password=passw, email=email
                )
                user1.save()
                username = User.objects.get(username=username)
                ob = userProfile.objects.create(user=username)
                ob.save()
                ob2 = customUser.objects.create(user=username)
                ob2.save()
                return render(request, "login.html")
        else:
            return render(request, "registertodo.html")

    else:
        return render(request, "registertodo.html")


@login_required(login_url="login")
def homePage(request):
    l = post.objects.all()
    username = request.session["user1"]
    user = User.objects.get(username=username)
    allusers = customUser.objects.exclude(id=user.customuser.id)
    return render(
        request,
        "instalikes.html",
        {"l": l, "username": username, "allusers": allusers,},
    )


@login_required(login_url="login")
def homepage_user(request, username):
    username_1 = request.session["user1"]
    user = User.objects.get(username=username_1)
    user2 = User.objects.get(username=username)
    if user.username == user2.username:
        return redirect("user_profile")
    else:
        num_of_friends = user2.customuser.friends.count()
        user3 = customUser.objects.get(id=user2.customuser.id)
        if FriendRequest.objects.filter(
            from_user=user.customuser.id, to_user=user3.id
        ).exists():
            friend = "requested"
        elif FriendRequest.objects.filter(
            from_user=user3.id, to_user=user.customuser.id
        ).exists():
            friend = "recieved"
        else:
            friend = "no"
        for i in user.customuser.friends.all():
            if i.user == user3.user:
                friend = "yes"
        if FriendRequest.objects.filter(
            from_user=user2.customuser.id, to_user=user.customuser.id
        ).exists():
            l = FriendRequest.objects.get(
                from_user=user2.customuser.id, to_user=user.customuser.id
            )
            frequestid = l.id
        else:
            frequestid = "none"
        return render(
            request,
            "randomuser_profile.html",
            {
                "friend": friend,
                "num_of_friends": num_of_friends,
                "user2": user2,
                "frequestid": frequestid,
            },
        )


"""checks for friend using ajax when page loads"""


@login_required(login_url="login")
def checkFriend(request):
    if request.method == "POST":
        username = request.session["user1"]
        user = User.objects.get(username=username)
        id = int(request.POST.get("id"))
        user2 = customUser.objects.get(id=id)
        for i in user.customuser.friends.all():
            if i.user == user2.user:
                return JsonResponse({"friend": "yes"})
        if FriendRequest.objects.filter(
            from_user=user.customuser.id, to_user=user2.id
        ).exists():
            return JsonResponse({"friend": "requested"})
        else:
            return JsonResponse({"friend": "no"})


"""removes a friend by user"""


@login_required(login_url="login")
def remove_friend(request):
    if request.method == "POST":
        id = int(request.POST.get("id"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        user1 = user.customuser
        user4 = customUser.objects.get(id=id)
        user1.friends.remove(user4)
        user4.friends.remove(user1)
        return JsonResponse({"status": "done"})


def increaseLikes(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        ob = post.objects.get(id=id)
        ob.likes = ob.likes + 1
        ob.save()
        user = request.session["user1"]
        liked_by = likedby(image=ob, name=user)
        liked_by.save()
        likes = ob.likes
        image = ob.image.url
        return JsonResponse({"likes": likes, "image": image})


def decreaseLikes(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        ob = post.objects.get(id=id)
        user = request.session["user1"]
        disliked = ob.likedby_set.get(name=user)
        disliked.delete()
        ob.likes = ob.likes - 1
        ob.save()
        likes = ob.likes
        image = ob.image.url
        return JsonResponse({"likes": likes, "image": image})


@login_required(login_url="login")
def checkForLike(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        ob = post.objects.get(id=id)
        user = request.session["user1"]
        if ob.likedby_set.filter(name=user).exists():
            return JsonResponse({"classname": "fas fa-heart"})
        else:
            return JsonResponse({"classname": "far fa-heart"})


@login_required(login_url="login")
def ajaxgetLikes(request):
    if request.method == "POST":
        names = []
        images = []
        id = int(request.POST.get("y"))
        ob = post.objects.get(id=id)
        usersLiked = ob.likedby_set.all()
        for i in usersLiked:
            user = User.objects.get(username=i.name)
            image = user.userprofile.image.url
            name = user.userprofile.name
            images.append(image)
            names.append(name)
        usersLiked = ob.likedby_set.all().values()
        return JsonResponse(
            {"usersLiked": list(usersLiked), "images": images, "names": names}
        )


@login_required(login_url="login")
def user_profile(request):
    username = request.session["user1"]
    user = User.objects.get(username=username)
    allfriends = user.customuser.friends.all()
    return render(request, "profile.html", {"user": user, "allfriends": allfriends})


@login_required(login_url="login")
def update_user(request):
    if request.method == "POST":
        username_changed = request.POST["username_changed"]
        username_before = request.session["user1"]
        user = User.objects.get(username=username_before)
        if (
            username_before != username_changed
            and User.objects.filter(username=username_changed).exists()
        ):
            allfriends = user.customuser.friends.all()
            return render(
                request,
                "profile.html",
                {
                    "user": user,
                    "allfriends": allfriends,
                    "message": "username already exists",
                },
            )
        else:
            email = request.POST["email"]
            name = request.POST["othername"]
            file = request.FILES.get("file_changed")
            if file is not None:
                user.userprofile.image = file
                user.userprofile.save()
            user.username = username_changed
            user.email = email
            user.userprofile.name = name
            user.userprofile.save()
            user.save()
            request.session["user1"] = username_changed
            return redirect("user_profile")


"""updates user bio from textarea via ajax when user clicks update-btn"""


@login_required(login_url="login")
def update_userdesc_ajax(request):
    if request.method == "POST":
        username = request.session["user1"]
        user = User.objects.get(username=username)
        desc = request.POST.get("bio")
        user.userprofile.desc = desc
        user.userprofile.save()
        return JsonResponse({"status": "done"})


@login_required(login_url="login")
def send_request(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        from_user = user.customuser
        to_user = customUser.objects.get(id=id)
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return HttpResponse("friend request sent")


@login_required(login_url="login")
def unsend_request(request):
    if request.method == "POST":
        id = int(request.POST.get("y"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        from_user = user.customuser
        to_user = customUser.objects.get(id=id)
        x = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
        x.delete()
        return HttpResponse("friend request sent")


@login_required(login_url="login")
def accept_request(request):
    if request.method == "POST":
        id = int(request.POST.get("id"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        user1 = user.customuser
        frequest = FriendRequest.objects.get(id=id)
        user2 = frequest.from_user
        user1.friends.add(user2)
        user2.friends.add(user1)
        ob = FriendRequest.objects.get(from_user=user2, to_user=user1)
        ob.delete()
        return redirect("user_profile")


@login_required(login_url="login")
def decline_request(request):
    if request.method == "POST":
        id = int(request.POST.get("id"))
        username = request.session["user1"]
        user = User.objects.get(username=username)
        user1 = user.customuser
        frequest = FriendRequest.objects.get(id=id)
        user2 = frequest.from_user
        ob = FriendRequest.objects.get(from_user=user2, to_user=user1)
        ob.delete()
        return redirect("user_profile")


@login_required(login_url="login")
def friend_requests(request):
    username = request.session["user1"]
    user = User.objects.get(username=username)
    frequests = FriendRequest.objects.filter(to_user=user.customuser.id)
    return render(request, "frequests.html", {"frequests": frequests})


"""seach user using ajax"""


@login_required(login_url="login")
def search_user(request):
    if request.method == "POST":
        images = []
        names = []
        value = request.POST.get("user")
        users = User.objects.filter(username__startswith=value)
        for i in users:
            image = i.userprofile.image.url
            images.append(image)
            name = i.userprofile.name
            names.append(name)
        users = User.objects.filter(username__startswith=value).values()[:4]
        return JsonResponse({"users": list(users), "images": images, "names": names})


"""create post """


def create_post(request):
    if request.method == "POST":
        username = request.session["user1"]
        user = User.objects.get(username=username)
        image = request.FILES["image"]
        figcaption = request.POST.get("figcaption")
        x = post(user=user, image=image, figcaption=figcaption)
        x.save()
        return HttpResponse("post created succesfully")
    else:
        return render(request, "post.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("login")
