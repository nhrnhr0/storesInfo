# Generated by Django 4.0.3 on 2022-03-13 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailResponse', models.JSONField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('place_id', models.CharField(max_length=200, unique=True)),
                ('types', models.JSONField()),
                ('vicinity', models.CharField(max_length=200)),
                ('x', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('y', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('businessStatus', models.CharField(blank=True, max_length=200, null=True)),
                ('permenentlyClose', models.BooleanField(default=False)),
                ('userRatingTotal', models.IntegerField(blank=True, null=True)),
                ('formated_phone', models.CharField(blank=True, max_length=200, null=True)),
                ('internal_phone', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('website', models.CharField(blank=True, max_length=200, null=True)),
                ('addressComponents', models.JSONField(blank=True, null=True)),
                ('nearbysearch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.nearbysearch')),
            ],
        ),
    ]
