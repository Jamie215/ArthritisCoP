# Generated by Django 4.2.6 on 2023-10-17 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('downvotes', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('downvotes', models.PositiveIntegerField(default=0)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='threads.thread')),
            ],
        ),
    ]