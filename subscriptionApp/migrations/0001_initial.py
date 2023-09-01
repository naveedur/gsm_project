# Generated by Django 4.2 on 2023-08-25 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gsmApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='credits_permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register', models.BooleanField(default=True, help_text='The user will receive credit when any user registers with his referral code.')),
                ('upload_Resource', models.BooleanField(default=True, help_text='The user will receive credit when they upload a file.')),
                ('upload_blog_post', models.BooleanField(default=True, help_text='The user will receive credit when they upload a post.')),
                ('referrad_credit_for_resource', models.BooleanField(default=False, help_text='The referred user will receive credit when their referrer upload a file.')),
                ('referrad_credit_for_blog_post', models.BooleanField(default=False, help_text='The referred user will receive credit when their referrer upload a post.')),
                ('referrad_credit_for_referrer_subsucription', models.BooleanField(default=False, help_text='The referred user will receive credit when their referrer buy subscription.')),
                ('referrad_credit_for_referrer_buying_file', models.BooleanField(default=False, help_text='The referred user will receive credit when their referrer buy a file.')),
            ],
        ),
        migrations.CreateModel(
            name='Single_File_Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_duration', models.CharField(default='', max_length=300)),
                ('duration', models.IntegerField(blank=True, default=0)),
                ('Price', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True)),
                ('Files_to_download', models.IntegerField(default=0)),
                ('Data_to_download', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credits', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='single_file_payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsmApp.resource')),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='pro_Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('files_download', models.IntegerField(blank=True, default=0, null=True)),
                ('data_download', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('subscription_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='subscriptionApp.subscription')),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='daily_download_limit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download_date', models.DateField(default=django.utils.timezone.now)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
