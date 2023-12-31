# Generated by Django 3.0.4 on 2020-04-03 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quartet_conductor', '0002_session_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='state',
            field=models.CharField(choices=[('RUNNING', 'Running'), ('PAUSED', 'Paused'), ('FINISHED', 'Finished')], default='RUNNING', help_text='The current state of the session.', max_length=50, verbose_name='State'),
        ),
    ]
