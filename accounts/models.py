from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() if full_name.strip() else self.username

    def __str__(self):
        return self.get_full_name() or self.username