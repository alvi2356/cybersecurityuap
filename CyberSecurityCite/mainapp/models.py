from django.db import models
import os


def user_image_path(instance, filename):
    # Generate path: media/users/user_<id>/<filename>
    ext = filename.split('.')[-1]
    filename = f"profile.{ext}"
    return os.path.join('users', f'user_{instance.userID}', filename)


class User(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
    )
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    passwordHash = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to=user_image_path, null=True, blank=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    teamMemberID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    socialLinks = models.TextField(blank=True)

    def __str__(self):
        return self.user.name


class Event(models.Model):
    eventID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    registrationDeadline = models.DateField()
    def __str__(self):
        return self.title

class Registration(models.Model):
    registrationID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registrationDate = models.DateField(auto_now_add=True)
    attended = models.BooleanField(default=False)


class Achievement(models.Model):
    achievementID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    dateAchieved = models.DateField()
    associatedUser = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class ContactForm(models.Model):
    formID = models.AutoField(primary_key=True)
    senderName = models.CharField(max_length=100)
    senderEmail = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submissionDate = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class FormerPresident(models.Model):
    formerPresidentID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    socialLinks = models.TextField(blank=True)

    def __str__(self):
        return self.user.name


# Add this to your models.py file

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    has_experience = models.BooleanField(default=False)
    expectations = models.TextField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"

    class Meta:
        unique_together = ('event', 'student_id')  # Prevent duplicate registrations