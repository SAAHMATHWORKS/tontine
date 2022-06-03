# Generated by Django 3.2.8 on 2022-05-31 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tontine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PretBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_pret', models.DateTimeField()),
                ('montant', models.PositiveIntegerField()),
                ('avaliseur', models.CharField(blank=True, max_length=50, null=True)),
                ('date_remboursement', models.DateTimeField()),
                ('taux_interet', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('versement_remboursement', models.PositiveIntegerField(default=0)),
                ('freeze', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tontine.membre')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilPretBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profil_pret', models.CharField(max_length=100, unique=True)),
                ('montant_min', models.PositiveIntegerField()),
                ('montant_max', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RemboursementPretBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_remboursement', models.DateTimeField()),
                ('montant', models.PositiveIntegerField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('pretbank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.pretbank')),
            ],
        ),
        migrations.AddField(
            model_name='pretbank',
            name='profil_pret_bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.profilpretbank'),
        ),
        migrations.CreateModel(
            name='EncaissementBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('operation', models.CharField(choices=[('DEPÔT', 'DEPÔT'), ('RETRAIT', 'RETRAIT'), ('INTERÊT', 'INTERÊT')], max_length=7)),
                ('montant', models.PositiveIntegerField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tontine.membre')),
            ],
        ),
    ]
