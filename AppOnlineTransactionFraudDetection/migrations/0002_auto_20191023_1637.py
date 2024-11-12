

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppOnlineTransactionFraudDetection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin_details',
            name='Aid',
            field=models.CharField(max_length=20),
        ),
    ]
