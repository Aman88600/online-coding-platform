from django.shortcuts import render, redirect, get_object_or_404
from .models import Coders, Problems
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'app_1/index.html')

def get_users():
    coders = Coders.objects.all()
    users = []
    for coder in coders:
        users.append(coder.username)
    return users

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # checking if user already exists
        users = get_users()
        if username in users:
            messages.error(request, "Username already exists! Please choose another.")
            return redirect('index')
        else:
            # Save new entry
            coder = Coders(username=username, email=email, password=password)
            coder.save()
        return redirect('dashboard')
    return redirect('index')
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Checking if the username exists
        try:
            Coders.objects.get(username=username)
            try:
                # checking if password is correct or not
                Coders.objects.get(password=password)
                request.session['username'] = username
                request.session['password'] = password
                return redirect('dashboard')
            except Coders.DoesNotExist:
                messages.error(request, "Password is incorrect")
                return redirect('index')
        except Coders.DoesNotExist:
            messages.error(request, "Username Does Not Exist, Sign Up First.")
            return redirect('index')
    return redirect('index')

def dashboard(request):
    if request.method == 'POST':
        del request.session['username']
        del request.session['password']
        request.session.clear()
        return redirect('index')

    elif request.method == 'GET':
        username = request.session.get('username') # if no username found then Guest is provided
        request.session.get('password')

        problems = Problems.objects.all()
        p_names = []
        for i in problems:
            p_names.append(i.problem_name)
        return render(request, 'app_1/dashboard.html', {'username':username, 'problems':p_names})
    username = request.session.get('username') # if no username found then Guest is provided
    request.session.get('password')

    problems = Problems.objects.all()
    p_names = []
    for i in problems:
        p_names.append(i.problem_name)
    return render(request, 'app_1/dashboard.html', {'username':username, 'problems':p_names})


def problems(request, problem_name):
    # Get the problem from the database
    problem = get_object_or_404(Problems, problem_name=problem_name)
    
    # Pass the problem object to the template
    return render(request, 'app_1/problem_detail.html', {'problem': problem})
