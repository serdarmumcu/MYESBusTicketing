# Generated by Django 2.2 on 2021-05-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busticket', '0010_auto_20210515_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_intent',
            field=models.CharField(default='', max_length=50),
        ),
    ]
