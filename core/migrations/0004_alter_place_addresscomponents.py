# Generated by Django 4.0.3 on 2022-03-13 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_place_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='addressComponents',
            field=models.TextField(blank=True, null=True),
        ),
    ]
