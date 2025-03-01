from django.shortcuts import render, redirect, get_object_or_404
from .models import Coders, Problems
from django.contrib import messages
import subprocess
import tempfile
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sys


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def list_to_linked_list(numbers):
    """ Converts a list of numbers into a linked list. """
    dummy = ListNode()
    current = dummy
    for num in numbers:
        current.next = ListNode(num)
        current = current.next
    return dummy.next

def linked_list_to_list(node):
    """ Converts a linked list into a list of numbers. """
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

@csrf_exempt
def run_code(request, problem_name):
    if request.method == "POST":
        code = request.POST.get("code", "")
        language = request.POST.get("language", "python")

        if not code:
            return JsonResponse({"error": "No code provided!"}, status=400)

        problem = Problems.objects.get(problem_name=problem_name)
        test_cases = problem.test_cases  # Retrieve stored test cases

        file_ext = {"python": ".py", "c": ".c", "cpp": ".cpp"}
        PYTHON_EXECUTABLE = "C:\\Users\\hp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"

        run_cmd = {
            "python": f"{PYTHON_EXECUTABLE} {{file}}",
            "c": "./{exe}",
            "cpp": "./{exe}"
        }

        results = []
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "solution" + file_ext[language])

            # ✅ Fix: Use UTF-8 encoding to prevent Unicode errors
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            for case in test_cases:
                raw_input = case["input"]
                expected_output = case["expected"]

                # 🔹 **Handle Linked List Problems**
                if "l1" in raw_input and "l2" in raw_input:
                    l1_str = " ".join(map(str, raw_input["l1"]))
                    l2_str = " ".join(map(str, raw_input["l2"]))
                    formatted_input = f"{l1_str}\n{l2_str}\n"
                    expected_output_str = " ".join(map(str, expected_output))
                else:
                    formatted_input = format_input(raw_input)
                    expected_output_str = format_output(expected_output)

                # Run the user's code with properly formatted input
                process = subprocess.run(
                    run_cmd[language].format(file=file_path),
                    input=formatted_input, text=True, shell=True, capture_output=True, timeout=5, encoding="utf-8"
                )

                actual_output = process.stdout.strip().replace(",", " ")  # Normalize output formatting

                results.append({
                    "input": formatted_input.strip(),
                    "expected": expected_output_str,
                    "actual": actual_output,
                    "pass": actual_output == expected_output_str,
                    "code": code
                })

        return JsonResponse({"results": results})

def format_input(raw_input):
    """ General input formatting. """
    if isinstance(raw_input, dict) and "nums" in raw_input and "target" in raw_input:
        nums_str = " ".join(map(str, raw_input["nums"]))
        return f"{nums_str}\n{raw_input['target']}\n"
    elif isinstance(raw_input, list):
        return "\n".join(" ".join(map(str, row)) for row in raw_input)
    return str(raw_input)

def format_output(expected_output):
    """ Converts expected output into a comparable string. """
    if isinstance(expected_output, list):
        return " ".join(map(str, expected_output))
    return str(expected_output)



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
