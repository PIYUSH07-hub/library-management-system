# Generated by Django 5.2.4 on 2025-07-18 11:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_remove_book_num_pages_remove_transaction_issue_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='pages',
        ),
        migrations.AddField(
            model_name='book',
            name='num_pages',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='issue_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.member'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='rent_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='transaction',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
