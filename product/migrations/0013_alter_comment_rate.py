# Generated by Django 3.2.4 on 2021-06-30 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.IntegerField(default=1),
        ),
    ]
