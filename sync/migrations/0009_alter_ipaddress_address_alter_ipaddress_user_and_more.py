# Generated by Django 4.0 on 2024-04-24 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sync', '0008_ipaddress_created_at_ipaddress_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipaddress',
            name='address',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='ipaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorized_ips', to='sync.mainuser'),
        ),
        migrations.AlterUniqueTogether(
            name='ipaddress',
            unique_together={('address', 'user')},
        ),
    ]