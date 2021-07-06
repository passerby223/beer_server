# Generated by Django 3.2.4 on 2021-06-08 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('creator', models.CharField(help_text='创建人', max_length=150, verbose_name='创建人')),
                ('modifier', models.CharField(help_text='最后修改人', max_length=150, verbose_name='最后修改人')),
                ('project_name', models.CharField(help_text='项目名称', max_length=150, verbose_name='项目名称')),
                ('project_desc', models.CharField(blank=True, default='', help_text='项目描述', max_length=256, verbose_name='项目描述')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
                'db_table': 'project_info',
            },
        ),
    ]
