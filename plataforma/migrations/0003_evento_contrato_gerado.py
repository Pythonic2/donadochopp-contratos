# Generated by Django 5.1.4 on 2025-01-05 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0002_contratopadrao'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='contrato_gerado',
            field=models.FileField(blank=True, null=True, upload_to='contratos_gerados/', verbose_name='Contrato Gerado'),
        ),
    ]
