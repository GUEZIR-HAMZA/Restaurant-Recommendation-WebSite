# Generated by Django 4.2 on 2023-05-14 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant_Recommendation_WebSite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='favorites',
            field=models.ManyToManyField(blank=True, to='Restaurant_Recommendation_WebSite.restaurant'),
        ),
    ]
