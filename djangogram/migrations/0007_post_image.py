# Generated by Django 4.1.1 on 2022-10-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogram', '0006_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
