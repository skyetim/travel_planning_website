# Generated by Django 2.1.7 on 2019-05-13 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('city_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('country_name', models.CharField(editable=False, max_length=20)),
                ('province_name', models.CharField(editable=False, max_length=20)),
                ('city_name', models.CharField(editable=False, max_length=20)),
                ('latitude', models.FloatField(editable=False)),
                ('longitude', models.FloatField(editable=False)),
            ],
        ),
        migrations.AddIndex(
            model_name='cities',
            index=models.Index(fields=['city_id'], name='C_cityid_idx'),
        ),
        migrations.AddIndex(
            model_name='cities',
            index=models.Index(fields=['country_name', 'province_name', 'city_name'], name='C_cityname_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='cities',
            unique_together={('country_name', 'province_name', 'city_name')},
        ),
    ]
