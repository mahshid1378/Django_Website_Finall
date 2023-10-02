# Generated by Django 2.2.11 on 2020-11-18 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_article_hits'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleHit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
                ('ip_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.IPAddress')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='hits',
            field=models.ManyToManyField(blank=True, related_name='hits', through='blog.ArticleHit', to='blog.IPAddress', verbose_name='Visits'),
        ),
    ]
