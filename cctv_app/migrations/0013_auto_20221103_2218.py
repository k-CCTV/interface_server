# Generated by Django 3.2.15 on 2022-11-03 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cctv_app', '0012_alter_board_detect_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='detact_result',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='board',
            name='detect_files',
            field=models.FileField(null=True, upload_to='detect/'),
        ),
    ]
