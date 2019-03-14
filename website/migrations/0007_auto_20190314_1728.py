# Generated by Django 2.1.7 on 2019-03-14 16:28

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20190314_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='liveblog',
            name='slack_channel',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='liveblog',
            name='body',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.StructBlock([('message_id', wagtail.core.blocks.CharBlock(required=False)), ('timestamp', wagtail.core.blocks.DateTimeBlock(required=False)), ('message', wagtail.core.blocks.CharBlock())])), ('image', wagtail.core.blocks.StructBlock([('message_id', wagtail.core.blocks.CharBlock(required=False)), ('timestamp', wagtail.core.blocks.DateTimeBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('embed', wagtail.core.blocks.StructBlock([('message_id', wagtail.core.blocks.CharBlock(required=False)), ('timestamp', wagtail.core.blocks.DateTimeBlock(required=False)), ('embed', wagtail.embeds.blocks.EmbedBlock())]))], blank=True),
        ),
    ]
