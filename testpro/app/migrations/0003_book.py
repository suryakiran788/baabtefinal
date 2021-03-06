# Generated by Django 3.0.8 on 2020-10-03 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_student_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.CharField(max_length=30)),
                ('department', models.CharField(max_length=30)),
                ('semester', models.ForeignKey(db_column='semester', on_delete=django.db.models.deletion.CASCADE, to='app.Student')),
            ],
        ),
    ]
