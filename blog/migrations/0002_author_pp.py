# Generated by Django 3.1.2 on 2020-10-13 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='pp',
            field=models.ImageField(default='images/default.jpg', upload_to='profile_pics'),
        ),
    ]
