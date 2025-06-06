# Generated by Django 4.2.3 on 2025-05-12 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gaharwb', '0015_alter_request_for_collaboration_otp_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/teams/', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/members/', verbose_name='تصویر'),
        ),
    ]
