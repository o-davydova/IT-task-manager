# Generated by Django 4.1 on 2023-10-04 18:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_hub", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["priority", "deadline"]},
        ),
        migrations.AlterField(
            model_name="task",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[("4", "Low"), ("3", "Medium"), ("2", "High"), ("1", "Urgent")],
                default="3",
                max_length=6,
            ),
        ),
    ]
