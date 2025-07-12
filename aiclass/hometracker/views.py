from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def react_home(request):
    return render(request, 'hometracker/index.html')
