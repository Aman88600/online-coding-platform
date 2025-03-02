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

        try:
            # Fetch the problem from the database
            problem = Problems.objects.get(problem_name=problem_name)

            # Check if test_cases is already a list
            if isinstance(problem.test_cases, str):
                # If it's a string, parse it as JSON
                test_cases = json.loads(problem.test_cases)
            else:
                # If it's already a list, use it directly
                test_cases = problem.test_cases

        except Problems.DoesNotExist:
            return JsonResponse({"error": "Problem not found!"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid test cases format!"}, status=500)

        # Define file extensions and execution commands
        file_ext = {"python": ".py", "c": ".c", "cpp": ".cpp"}
        PYTHON_EXECUTABLE = "C:\\Users\\hp\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        
        run_cmd = {
            "python": f"{PYTHON_EXECUTABLE} {{file}}",
            "c": "gcc {file} -o {exe} && {exe}",
            "cpp": "g++ {file} -o {exe} && {exe}"
        }
        
        results = []
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "solution" + file_ext[language])
            
            # Write the code to a temporary file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Handle compilation for C/C++
            if language in ["c", "cpp"]:
                exe_path = os.path.join(temp_dir, "a.exe" if language == "c" else "a.out")
                command = run_cmd[language].format(file=file_path, exe=exe_path)
            else:
                command = run_cmd[language].format(file=file_path)
            print(test_cases)
            # Run the code against each test case
            for case in test_cases:
                raw_input = case["input"]
                expected_output = case["expected"]
                print(f"raw_input = {raw_input}")
                # Format the input
                if isinstance(raw_input, dict):
                    formatted_input = "\n".join(map(str, raw_input.values())) + "\n"
                else:
                    formatted_input = str(raw_input) + "\n"
                print(f"Formatted = {formatted_input}")
                # Format the expected output
                expected_output_str = " ".join(map(str, expected_output))

                # Execute the code
                process = subprocess.run(
                    command,
                    input=formatted_input, text=True, shell=True, capture_output=True, timeout=5, encoding="utf-8"
                )
                
                # Format the actual output
                actual_output = process.stdout.strip().replace(",", " ")
                print(actual_output)
                # Append the result
                results.append({
                    "input": formatted_input.strip(),
                    "expected": expected_output_str,
                    "actual": actual_output,
                    "pass": actual_output == expected_output_str,
                    "code": code,
                    "stderr": process.stderr.strip() if process.stderr else ""
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
