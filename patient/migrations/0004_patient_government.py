# Generated by Django 3.0.5 on 2023-03-08 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20230308_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='government',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/government/'),
        ),
    ]