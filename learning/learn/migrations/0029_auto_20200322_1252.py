# Generated by Django 3.0.3 on 2020-03-22 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0028_about_admin_registration_blogs_certificates_course_chapter_course_chapter_content_enrollment_exam_ex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher_registration',
            name='Image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
