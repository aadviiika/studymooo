from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        # Remove old Resource fields
        migrations.RemoveField(model_name='resource', name='course'),
        migrations.RemoveField(model_name='resource', name='subject'),
        # Remove Course model
        migrations.DeleteModel(name='Course'),
        # Add new Resource fields
        migrations.AddField(
            model_name='resource',
            name='course_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='resource',
            name='notes_type',
            field=models.CharField(
                choices=[
                    ('Lecture Notes', 'Lecture Notes'),
                    ('Textbook', 'Textbook'),
                    ('Question Bank', 'Question Bank'),
                    ('Sample Paper', 'Sample Paper'),
                ],
                default='Lecture Notes',
                max_length=50,
            ),
        ),
        # Remove avatar_initial_color from Profile
        migrations.RemoveField(
            model_name='profile',
            name='avatar_initial_color',
        ),
    ]