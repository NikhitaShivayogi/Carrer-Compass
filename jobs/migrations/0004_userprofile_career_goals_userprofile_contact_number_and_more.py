# Generated by Django 5.1.7 on 2025-05-15 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='career_goals',
            field=models.TextField(blank=True, help_text="User's career aspirations or goals", null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='contact_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='education',
            field=models.CharField(blank=True, help_text='E.g., BCA, MCA', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='experience_level',
            field=models.CharField(choices=[('Fresher', 'Fresher'), ('Junior', 'Junior'), ('Mid', 'Mid-Level'), ('Senior', 'Senior')], default='Fresher', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='github_url',
            field=models.URLField(blank=True, help_text='Link to GitHub profile', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='linkedin_url',
            field=models.URLField(blank=True, help_text='Link to LinkedIn profile', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='portfolio_url',
            field=models.URLField(blank=True, help_text='Link to personal portfolio', null=True),
        ),
    ]
