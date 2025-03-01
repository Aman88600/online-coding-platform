# Generated by Django 5.1.6 on 2025-02-26 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0002_problems'),
    ]

    operations = [
        migrations.AddField(
            model_name='problems',
            name='difficulty_level',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Medium', max_length=50),
        ),
        migrations.AddField(
            model_name='problems',
            name='example_explanation',
            field=models.TextField(default='Explanation for the example.'),
        ),
        migrations.AddField(
            model_name='problems',
            name='example_input',
            field=models.TextField(default='Example input here'),
        ),
        migrations.AddField(
            model_name='problems',
            name='example_output',
            field=models.TextField(default='Example output here'),
        ),
        migrations.AddField(
            model_name='problems',
            name='function_signature',
            field=models.TextField(default='def function_name():'),
        ),
        migrations.AddField(
            model_name='problems',
            name='solution',
            field=models.TextField(blank=True, default='No solution provided yet.', null=True),
        ),
        migrations.AlterField(
            model_name='problems',
            name='problem_description',
            field=models.TextField(default='No description provided'),
        ),
        migrations.AlterField(
            model_name='problems',
            name='problem_name',
            field=models.CharField(default='Untitled Problem', max_length=255),
        ),
    ]
