# Generated by Django 2.1.7 on 2019-03-14 13:47

import datetime
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import website.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_Add snippet model'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_id', models.CharField(max_length=40)),
                ('raw_update', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='liveblog',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(1980, 1, 1, 0,
                                                                 0)),
        ),
        migrations.AlterField(
            model_name='liveblog',
            name='body',
            field=wagtail.core.fields.StreamField([('embed', website.blocks.Embed()), ('text', wagtail.core.blocks.StructBlock([('message_id', wagtail.core.blocks.CharBlock()), ('timestamp', wagtail.core.blocks.DateTimeBlock()), ('message', wagtail.core.blocks.CharBlock())]))], blank=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='live_updates', to='website.LiveBlog'),
        ),
        migrations.AddField(
            model_name='pendingupdate',
            name='live_blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.LiveBlog'),
        ),
    ]
