# Generated by Django 4.2.3 on 2023-07-28 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=100)),
                ('completion_date', models.DateField()),
                ('certificate_code', models.CharField(max_length=10, unique=True)),
            ],
        ),
    ]