# Generated by Django 3.2.5 on 2021-10-03 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abash', '0005_auto_20210930_2332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='city',
            new_name='upazila',
        ),
    ]
