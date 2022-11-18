# Generated by Django 4.1.3 on 2022-11-16 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
        ('users', '0003_alter_user_entity_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='entities.entity'),
        ),
    ]
