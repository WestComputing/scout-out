# Generated by Django 3.0.8 on 2020-07-27 13:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scout', '0002_auto_20200726_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGeolocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(default='Home', max_length=50)),
                ('geolocation',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='geolocations',
                                   to='scout.Geolocation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'label')},
            },
        ),
    ]
