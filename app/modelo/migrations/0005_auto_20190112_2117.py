# Generated by Django 2.1.4 on 2019-01-12 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0004_auto_20190109_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bancavirtual',
            name='numeroCuentaDestino',
            field=models.CharField(max_length=20),
        ),
    ]
