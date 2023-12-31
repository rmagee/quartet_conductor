# Generated by Django 3.0.4 on 2020-04-13 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quartet_capture', '0010_auto_20200401_2145'),
        ('quartet_conductor', '0005_auto_20200411_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputmap',
            name='input_number',
            field=models.PositiveSmallIntegerField(default=7, help_text='The input number to map the rule and input text to.', verbose_name='Input Number'),
        ),
        migrations.AddField(
            model_name='inputmap',
            name='related_session_input',
            field=models.PositiveSmallIntegerField(blank=True, help_text="If a session is started via another input and that session contains data necessary for this mapping input map's rule to run then assign that input here.", null=True, verbose_name='Related Session Input'),
        ),
        migrations.AddField(
            model_name='inputmap',
            name='rule',
            field=models.ForeignKey(default=1, help_text='The rule to execute when the input is high.', on_delete=django.db.models.deletion.CASCADE, to='quartet_capture.Rule', verbose_name='Rule'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inputmap',
            name='rule_data',
            field=models.TextField(blank=True, help_text='Any data to send to the rule when running it. The formatdepends on what the rule expects. ', null=True, verbose_name='Rule Data'),
        ),
    ]
