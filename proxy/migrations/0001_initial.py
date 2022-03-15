# Generated by Django 4.0.3 on 2022-03-15 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20)),
                ('port', models.CharField(max_length=20)),
                ('isWorking', models.BooleanField(default=True)),
                ('last_checked', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
