# Generated by Django 2.0.7 on 2018-08-14 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20180814_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(help_text='Enter your blog text here.', max_length=2000),
        ),
    ]
