# Generated by Django 4.2.7 on 2024-05-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rating_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(null=True, upload_to='service/'),
        ),
    ]