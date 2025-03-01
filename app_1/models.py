from django.db import models

# Create your models here.
class Coders(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"username = {self.username} email = {self.email} password = {self.password}"

from django.db import models

class Problems(models.Model):
    # Basic problem details
    problem_name = models.CharField(max_length=255, default="Untitled Problem")  # Default name if not provided
    problem_description = models.TextField(default="No description provided")  # Default description
    function_signature = models.TextField(default="def function_name():")  # Default function signature template

    # Examples of inputs/outputs
    example_input = models.TextField(default="Example input here")  # Default example input
    example_output = models.TextField(default="Example output here")  # Default example output
    example_explanation = models.TextField(default="Explanation for the example.")  # Default explanation

    # Additional fields if needed
    difficulty_level = models.CharField(max_length=50, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Medium')

    # Optional: Solution or hints for the problem (You can leave it empty or add later)
    solution = models.TextField(blank=True, null=True, default="No solution provided yet.")  # Default solution if not provided

    def __str__(self):
        return f"Problem: {self.problem_name}"


