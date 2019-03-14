# Generated by Django 2.1.7 on 2019-03-13 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_liveblog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=255)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.LiveBlog')),
            ],
        ),
    ]