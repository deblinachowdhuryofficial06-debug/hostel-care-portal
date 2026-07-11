
from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    # These are the choices for the status of a complaint
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    # Links the complaint to a specific registered student user
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The fields containing the complaint data
    title = models.CharField(max_length=200)
    description = models.TextField()
    room_number = models.CharField(max_length=10)
    
    # Auto_now_add automatically records the exact time it was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Status starts as 'Pending' automatically
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Image field (blank=True, null=True means the image is optional)
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.student.username}"

class Comment(models.Model):
    # This links the comment directly to a specific Complaint row
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    # This tracks who wrote it (can be a student or a warden)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.complaint.title}"