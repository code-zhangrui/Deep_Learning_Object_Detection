# Generated by Django 2.0.6 on 2018-11-16 06:22

import detect.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=detect.models.save_cards)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=detect.models.save_papers)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=200)),
                ('join_time', models.DateTimeField(verbose_name='join time')),
                ('profile_photo', models.ImageField(upload_to='players')),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detect.Player'),
        ),
        migrations.AddField(
            model_name='card',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detect.Player'),
        ),
    ]
