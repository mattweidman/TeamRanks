# Generated by Django 2.0.1 on 2018-01-25 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='id',
        ),
        migrations.AddField(
            model_name='preference',
            name='prefid',
            field=models.CharField(default='', max_length=256, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
