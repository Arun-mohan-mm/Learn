# Generated by Django 3.0.3 on 2020-03-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0033_auto_20200325_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_chapter_content',
            name='Is_image',
        ),
        migrations.RemoveField(
            model_name='course_chapter_content',
            name='Is_paragraph',
        ),
        migrations.RemoveField(
            model_name='course_chapter_content',
            name='Is_video',
        ),
        migrations.AddField(
            model_name='course_chapter_content',
            name='Content_type',
            field=models.CharField(max_length=200),
            preserve_default=False,
        ),
    ]
