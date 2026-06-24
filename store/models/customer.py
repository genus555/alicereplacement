from django.db import models

class Customer(models.Model):
    ign = models.CharField(max_length=50)
    discord_name = models.CharField(max_length=50)

    def register(self):
        self.save()
    
    @staticmethod
    def get_customer_by_in_game_name(ign):
        try:
            return Customer.objects.get(ign=ign)
        except Customer.DoesNotExist:
            return False
    
    def isExists(self):
        return Customer.objects.filter(ign=self.ign).exists()
    
    class Meta:
        verbose_name_plural = "Customers"
    
    def __str__(self):
        return f"{self.ign} | {self.discord_name}"