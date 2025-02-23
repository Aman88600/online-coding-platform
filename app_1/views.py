from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'app_1/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f'{username} {email} {password}')

    # return render(request, 'app_1/index.html')
    return redirect('index')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f'{username} {password}')

    # return render(request, 'app_1/index.html')
    return redirect('index')