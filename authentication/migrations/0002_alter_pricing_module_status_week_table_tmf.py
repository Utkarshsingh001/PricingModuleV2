# Generated by Django 4.2.4 on 2023-08-08 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricing_module',
            name='status',
            field=models.BooleanField(),
        ),
        migrations.CreateModel(
            name='Week_Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.TextField(max_length=200)),
                ('mod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.pricing_module')),
            ],
        ),
        migrations.CreateModel(
            name='TMF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField()),
                ('factor', models.FloatField()),
                ('mod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.pricing_module')),
            ],
        ),
    ]
