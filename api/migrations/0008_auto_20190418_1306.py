# Generated by Django 2.1.3 on 2019-04-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190409_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getadesarunlist',
            name='MMR',
            field=models.TextField(default='n/a'),
        ),
        migrations.AlterField(
            model_name='getadesarunlist',
            name='check',
            field=models.TextField(default='n/a'),
        ),
        migrations.AlterField(
            model_name='getadesarunlist',
            name='extra',
            field=models.TextField(default='n/a'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='MMR',
            field=models.TextField(default='n/a'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='check',
            field=models.TextField(default='n/a'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='extra',
            field=models.TextField(default='n/a'),
        ),
    ]