# Generated by Django 3.2.15 on 2022-10-04 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cctv_app', '0008_board_detect_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='detect_files',
            field=models.FileField(null=True, upload_to='detect_urlpatterns'),
        ),
    ]
