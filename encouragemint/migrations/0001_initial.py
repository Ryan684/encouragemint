# Generated by Django 2.2.7 on 2019-11-23 17:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_id', models.UUIDField(default=uuid.uuid4)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_id', models.UUIDField(default=uuid.uuid4)),
                ('plant_name', models.CharField(max_length=25)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encouragemint.Profile')),
            ],
        ),
    ]
