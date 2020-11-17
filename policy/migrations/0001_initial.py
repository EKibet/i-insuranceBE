# Generated by Django 3.1.3 on 2020-11-17 10:58

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('bio', models.TextField(blank=True, max_length=500, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='CommonUserFieldMixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('id_no', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_number', models.CharField(max_length=20)),
                ('policy_contact', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('form', models.TextField(max_length=300)),
                ('slug', models.SlugField(max_length=200)),
                ('signed', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-signed',),
                'index_together': {('id', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('commonuserfieldmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policy.commonuserfieldmixin')),
                ('id_img', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('profile_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex/Parody')], max_length=1)),
                ('employment_status', models.CharField(choices=[('E', 'Employed'), ('U', 'Unemployed'), ('S', 'Self-employed')], max_length=1)),
                ('bank_accountno', models.IntegerField(default=0)),
                ('policy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userprofile', to='policy.policy')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('policy.commonuserfieldmixin',),
        ),
        migrations.CreateModel(
            name='AgentProfile',
            fields=[
                ('commonuserfieldmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policy.commonuserfieldmixin')),
                ('cv', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('profile_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('job_number', models.CharField(max_length=20, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex/Parody')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('policy.commonuserfieldmixin',),
        ),
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('commonuserfieldmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policy.commonuserfieldmixin')),
                ('cv', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('profile_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('remarks', models.TextField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('policy.commonuserfieldmixin',),
        ),
    ]
