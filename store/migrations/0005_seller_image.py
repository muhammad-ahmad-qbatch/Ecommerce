# Generated by Django 4.0.5 on 2022-09-22 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_vendor_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
