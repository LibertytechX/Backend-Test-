# Generated by Django 4.0.1 on 2022-04-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_allcoins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allcoins',
            name='usd_price',
            field=models.CharField(default=0, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='allcoins',
            name='volume',
            field=models.CharField(default=0, max_length=255, null=True),
        ),
    ]
