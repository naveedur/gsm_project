# Generated by Django 4.2 on 2023-08-25 11:55

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
            name='article',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('desc', models.TextField()),
                ('verified', models.BooleanField(default=False)),
                ('view_count', models.IntegerField(blank=True, default=0)),
                ('slug', models.SlugField(blank=True, default='')),
                ('Model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gsmApp.model')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('sno',),
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('categorypost', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gsmApp.category')),
                ('modelpost', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gsmApp.model')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blogApp.blogcomment')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blogApp.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
