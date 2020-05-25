from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import usersidle
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, "chatapp2home.html")


@csrf_exempt
def room(request):
    if request.method == "POST":
        person_name = request.POST["username"]
        request.session["user"] = person_name
        return render(request, "chatapp2.html", {"person_name": person_name})


@csrf_exempt
def checkForIdle(request):
    num_of_users = usersidle.objects.count()
    if num_of_users == 0:
        username = request.session["user"]
        roomid = random.randint(1, 10000000)
        roomname = "room" + str(roomid)
        usersidle.objects.create(name=username, roomid=roomname)
        return JsonResponse({"roomname": roomname, "status": "idle"})
    else:
        user = usersidle.objects.all()
        randomuser = user[0]
        roomname = randomuser.roomid
        username = randomuser.name
        user[0].delete()
        return JsonResponse(
            {"roomname": roomname, "status": "connected", "username": username}
        )
