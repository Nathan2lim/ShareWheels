# Generated by Django 5.1.4 on 2025-01-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='prenom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
