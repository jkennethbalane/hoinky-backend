# Generated by Django 5.0.6 on 2024-07-29 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HoinkyPass', '0002_alter_hoinkyuser_quests_achieved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoinkyuser',
            name='quests_achieved',
            field=models.ManyToManyField(blank=True, to='HoinkyPass.quest'),
        ),
    ]