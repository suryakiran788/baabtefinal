# Generated by Django 3.0.8 on 2020-10-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_book_bookfilename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='bookfilename',
            field=models.CharField(max_length=250),
        ),
    ]
