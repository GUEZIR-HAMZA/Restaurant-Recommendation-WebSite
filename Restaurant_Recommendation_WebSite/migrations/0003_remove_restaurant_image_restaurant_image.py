# Generated by Django 4.2 on 2023-05-14 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant_Recommendation_WebSite', '0002_alter_users_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='image',
        ),
        migrations.CreateModel(
            name='restaurant_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='restaurants')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Restaurant_Recommendation_WebSite.restaurant')),
            ],
        ),
    ]