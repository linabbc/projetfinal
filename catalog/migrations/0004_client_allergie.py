# Generated by Django 3.0.5 on 2020-05-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200511_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='allergie',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
