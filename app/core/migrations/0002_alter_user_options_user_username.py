# Generated by Django 4.0.1 on 2022-04-29 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='toluliberty', max_length=25, unique=True),
            preserve_default=False,
        ),
    ]