# Generated by Django 5.1.5 on 2025-02-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalinfo',
            name='icon',
            field=models.CharField(default='tag', max_length=20),
        ),
    ]
