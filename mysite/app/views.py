from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import random
# Create your views here.
def home(request):
    return render(request,'home.html')
def number(request):
    random_no=random.randint(1,10)
    return JsonResponse({'random_no':random_no})
    