from django.shortcuts import render


# Create your views here.

def index(request):
    # Add all details into dict
    dict = {}
    return render(request, 'wbl/index.html', dict)


def dashboard(request):
    return render(request, 'wbl/dashboard.html')


def tasks(request):
    return render(request, 'wbl/tasks.html')
