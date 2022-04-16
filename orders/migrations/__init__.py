from django.db import migrations, models
from users.models import User

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True)),
                ('price', models.IntegerField(max_length=100)),
                ('user', models.IntegerField()),
                ('is_active', models.BooleanField())
            ]
        )
    ]