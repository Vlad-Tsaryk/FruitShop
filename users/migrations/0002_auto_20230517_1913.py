# Generated by Django 3.2.19 on 2023-05-17 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterField(
            model_name="message",
            name="text",
            field=models.CharField(max_length=255),
        ),
    ]
