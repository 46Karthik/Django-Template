from django.db import models
from django.contrib.auth.models import User as AuthUser

# example JSON data for creating a user profile
# {
#   "username": "admin",
#   "email": "admin@example.com",
#   "password": "admin@123",
#   "phone": "1234567890",
#   "role_id": 1
# }


# INSERT INTO myapp_role (name) VALUES 
#     ('Super Admin'),
#     ('Admin'),
#     ('company')


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles')  # New field
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name or self.user.username