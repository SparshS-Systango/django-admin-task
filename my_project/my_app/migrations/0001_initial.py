# Generated by Django 4.0.1 on 2023-05-30 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.TextField(blank=True, default='', max_length=30, null=True)),
                ('hidden_field', models.CharField(max_length=40)),
                ('users', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.TextField(blank=True, default='', max_length=30, null=True)),
                ('economic_model', models.CharField(default='partnership', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='VendorPricingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('economic_model', models.CharField(default='retrocom', max_length=20)),
                ('product_name', models.CharField(blank=True, default='', max_length=200)),
                ('yavin_fee', models.IntegerField()),
                ('suggested_fee', models.IntegerField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_pricing_plans', to='my_app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='PricingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('fee', models.IntegerField()),
                ('scope', models.CharField(max_length=50)),
                ('status', models.CharField(default='open', max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricingplans', to='my_app.company')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to='my_app.vendor'),
        ),
    ]
