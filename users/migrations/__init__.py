from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('second_name', models.CharField(max_length=100)),
                ('balance', models.IntegerField())
            ]
        )
    ]