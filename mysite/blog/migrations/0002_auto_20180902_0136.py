# Generated by Django 2.0 on 2018-09-01 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='type_name',
            new_name='blog_type',
        ),
    ]