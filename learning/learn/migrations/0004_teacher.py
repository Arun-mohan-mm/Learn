# Generated by Django 3.0.2 on 2020-01-09 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_subject_details_teacher_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=200)),
                ('teacher_topic', models.CharField(max_length=200)),
            ],
        ),
    ]
