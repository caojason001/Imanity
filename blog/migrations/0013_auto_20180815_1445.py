# Generated by Django 2.0.7 on 2018-08-15 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_blog_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='blog_title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='title',
        ),
    ]
