# Generated by Django 2.2.5 on 2019-10-14 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caminho', models.CharField(max_length=64)),
                ('pagina', models.CharField(max_length=50)),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Texto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagina', models.CharField(max_length=64)),
                ('numero', models.IntegerField()),
                ('texto', models.TextField()),
            ],
        ),
    ]
