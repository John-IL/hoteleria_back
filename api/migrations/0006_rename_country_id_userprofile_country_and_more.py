# Generated by Django 4.1.7 on 2023-04-06 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_country_userprofile_country_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='country_id',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='personal_id',
            new_name='personal',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='role_id',
            new_name='role',
        ),
    ]
