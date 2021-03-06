# Generated by Django 3.1.4 on 2020-12-17 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0004_auto_20201217_1511'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Lable',
            new_name='Label',
        ),
        migrations.RemoveField(
            model_name='host',
            name='lables',
        ),
        migrations.AddField(
            model_name='host',
            name='labels',
            field=models.ManyToManyField(blank=True, to='cmdb.Label', verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='historicalhost',
            name='hostname',
            field=models.CharField(blank=True, max_length=50, verbose_name='主机名'),
        ),
        migrations.AlterField(
            model_name='historicalhost',
            name='offline_date',
            field=models.DateField(blank=True, null=True, verbose_name='下架日期'),
        ),
        migrations.AlterField(
            model_name='historicalhost',
            name='online_date',
            field=models.DateField(blank=True, null=True, verbose_name='上架日期'),
        ),
        migrations.AlterField(
            model_name='host',
            name='hostname',
            field=models.CharField(blank=True, max_length=50, verbose_name='主机名'),
        ),
        migrations.AlterField(
            model_name='host',
            name='offline_date',
            field=models.DateField(blank=True, null=True, verbose_name='下架日期'),
        ),
        migrations.AlterField(
            model_name='host',
            name='online_date',
            field=models.DateField(blank=True, null=True, verbose_name='上架日期'),
        ),
    ]
