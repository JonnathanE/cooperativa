# Generated by Django 2.1.4 on 2019-01-13 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0005_auto_20190112_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='tipo',
            field=models.CharField(choices=[('retiro', 'Retiro'), ('deposito', 'Depósito'), ('transferencia', 'Transferencia')], max_length=30),
        ),
    ]
