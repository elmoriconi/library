# Generated by Django 5.0.6 on 2024-06-23 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_member_assigned'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='member',
            constraint=models.UniqueConstraint(fields=('member_id',), name='unique_member_id'),
        ),
    ]
