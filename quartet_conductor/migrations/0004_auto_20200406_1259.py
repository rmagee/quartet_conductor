# Generated by Django 3.0.4 on 2020-04-06 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quartet_conductor', '0003_session_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='lot',
            field=models.CharField(help_text='The session lot number', max_length=20, unique=True, verbose_name='Lot'),
        ),
    ]
