# Generated by Django 3.2.4 on 2021-06-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_sliderimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='slider_image/')),
            ],
        ),
    ]