# Generated by Django 3.0.5 on 2020-05-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_client_allergie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='allergie',
            new_name='medicament',
        ),
        migrations.AddField(
            model_name='client',
            name='besoin_particulier',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
