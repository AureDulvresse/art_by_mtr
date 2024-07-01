from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"