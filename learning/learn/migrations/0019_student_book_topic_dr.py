# Generated by Django 3.0.2 on 2020-02-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0018_auto_20200204_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_book',
            name='topic_dr',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
