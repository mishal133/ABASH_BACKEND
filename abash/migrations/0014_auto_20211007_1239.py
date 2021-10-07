# Generated by Django 3.2.5 on 2021-10-07 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abash', '0013_auto_20211007_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='received_booking',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abash.property'),
        ),
        migrations.AlterField(
            model_name='received_booking',
            name='requested_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abash.user_details'),
        ),
    ]
