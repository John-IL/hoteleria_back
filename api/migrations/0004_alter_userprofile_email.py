# Generated by Django 4.1.7 on 2023-04-06 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=45, unique=True),
        ),
    ]
