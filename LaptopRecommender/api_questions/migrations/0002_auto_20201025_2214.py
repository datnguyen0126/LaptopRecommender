# Generated by Django 3.0.8 on 2020-10-25 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='answers',
            table='answers',
        ),
        migrations.AlterModelTable(
            name='questions',
            table='questions',
        ),
    ]
