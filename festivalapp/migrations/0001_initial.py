# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-26 21:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import festivalapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to=festivalapp.models.get_logo_path, verbose_name='Logo')),
                ('anio', models.IntegerField(choices=[(2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)], default=2017, verbose_name='A\xf1o')),
                ('fechinicio', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha inicio de inscripci\xf3n')),
                ('fechinscrip', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha l\xedmite de inscripci\xf3n')),
                ('titulo', models.CharField(max_length=100, null=True)),
                ('descripcion', models.TextField(default='', max_length=500, verbose_name='Descripci\xf3n')),
            ],
        ),
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, null=True)),
                ('tituloesp', models.CharField(max_length=100, null=True)),
                ('tituloing', models.CharField(max_length=100, null=True)),
                ('duracion', models.IntegerField(null=True)),
                ('video', models.CharField(max_length=15, null=True)),
                ('nacionalidad', models.CharField(max_length=100, null=True)),
                ('paisrodaje', models.CharField(max_length=100, null=True)),
                ('aniorodaje', models.IntegerField(null=True)),
                ('formatorodaje', models.CharField(max_length=100, null=True)),
                ('montaje', models.CharField(max_length=100, null=True)),
                ('produccion', models.CharField(max_length=100, null=True)),
                ('sonido', models.CharField(max_length=100, null=True)),
                ('musica', models.CharField(max_length=100, null=True)),
                ('idiomaoriginal', models.CharField(max_length=100, null=True)),
                ('subtitulos', models.CharField(max_length=100, null=True)),
                ('actores', models.TextField(null=True)),
                ('enlacevisionado', models.URLField(null=True)),
                ('enlacetrailer', models.URLField(null=True)),
                ('enlaceproyeccion', models.URLField(null=True)),
                ('enlacedescarga', models.URLField(null=True)),
                ('image', models.ImageField(upload_to=festivalapp.models.get_file_path)),
                ('guion', models.CharField(max_length=1000, null=True)),
                ('sinopsing', models.CharField(max_length=1000, null=True)),
                ('sinopsisesp', models.CharField(max_length=1000, null=True)),
                ('lugarestreno1', models.CharField(max_length=100, null=True)),
                ('fechaestrenointer', models.DateField(null=True)),
                ('lugarestrenoesp', models.CharField(max_length=100, null=True)),
                ('fechaestrenoesp', models.DateField(null=True)),
                ('web', models.URLField(null=True)),
                ('premios', models.CharField(max_length=500, null=True)),
                ('comentarios', models.CharField(max_length=500, null=True)),
                ('secciones', models.TextField(null=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('participante', models.BooleanField(default=False)),
                ('premiada', models.BooleanField(default=False)),
                ('festival', models.IntegerField(default=2017)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, null=True)),
                ('telefono', models.CharField(max_length=13, null=True)),
                ('apellidos', models.CharField(max_length=60, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proyeccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('horaInicio', models.TimeField(null=True)),
                ('horaFin', models.TimeField(null=True)),
                ('orderdate', models.DateTimeField(null=True)),
                ('pelicula', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Pelicula')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('festival', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='festivalapp.Festival')),
                ('visibilidad', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='festival',
            name='secciones',
            field=models.ManyToManyField(blank=True, to='festivalapp.Seccion'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Question'),
        ),
        migrations.AddField(
            model_name='proyeccion',
            name='prog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Programa'),
        ),
        migrations.AddField(
            model_name='programa',
            name='proyecciones',
            field=models.ManyToManyField(blank=True, to='festivalapp.Proyeccion'),
        ),
    ]
