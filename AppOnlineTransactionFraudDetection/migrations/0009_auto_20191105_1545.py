# Generated by Django 2.1.5 on 2019-11-05 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppOnlineTransactionFraudDetection', '0008_auto_20191104_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='Securityanswer1',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='user_details',
            name='Securityanswer2',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='user_details',
            name='Securityanswer3',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='user_details',
            name='Securityquestion1',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='user_details',
            name='Securityquestion2',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='user_details',
            name='Securityquestion3',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
