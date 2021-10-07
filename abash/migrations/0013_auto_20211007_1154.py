# Generated by Django 3.2.5 on 2021-10-07 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abash', '0012_auto_20211007_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='rented_property',
            name='agreement_type',
            field=models.CharField(choices=[('M', 'Monthly'), ('W', 'Weekly'), ('D', 'Daily')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='rented_property',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='rented_property',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]