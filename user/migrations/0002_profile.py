# Generated by Django 2.0.7 on 2019-02-13 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dating_sex', models.CharField(choices=[('male', '男性'), ('female', '女性')], max_length=8, verbose_name='匹配的性别')),
                ('location', models.CharField(choices=[('bj', '北京'), ('sh', '上海'), ('gz', '广州'), ('sz', '深圳'), ('cd', '成都'), ('xa', '西安'), ('wh', '武汉')], max_length=16, verbose_name='目标城市')),
                ('min_distance', models.IntegerField(default=1, verbose_name='最小查找范围')),
                ('max_distance', models.IntegerField(default=10, verbose_name='最大查找范围')),
                ('min_dating_age', models.IntegerField(default=18, verbose_name='最小交友年龄')),
                ('max_dating_age', models.IntegerField(default=50, verbose_name='最大交友年龄')),
                ('vibration', models.BooleanField(default=True, verbose_name='开启震动')),
                ('only_matche', models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')),
                ('auto_play', models.BooleanField(default=True, verbose_name='自动播放视频')),
            ],
        ),
    ]
