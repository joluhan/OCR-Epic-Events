# Generated by Django 5.0.2 on 2024-04-11 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epicevents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('sales', 'Sales'), ('support', 'Support'), ('management', 'Management')], default='management', max_length=20),
        ),
    ]
