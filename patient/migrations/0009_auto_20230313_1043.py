# Generated by Django 3.0.5 on 2023-03-13 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0008_auto_20230313_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='profile_pic1',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/government/'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/Patient/'),
        ),
    ]