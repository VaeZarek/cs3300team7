# Generated by Django 5.2 on 2025-04-16 04:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='applications/')),
                ('cover_letter', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('shortlisted', 'Shortlisted'), ('interviewing', 'Interviewing'), ('offered', 'Offered'), ('rejected', 'Rejected')], default='pending', max_length=50)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='applicant.applicantprofile')),
            ],
        ),
    ]
