# Generated by Django 4.0.3 on 2022-03-15 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_easypage_hasdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='easypage',
            name='html',
            field=models.TextField(blank=True, null=True),
        ),
    ]