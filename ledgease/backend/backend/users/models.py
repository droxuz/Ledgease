from django.db import models

# Create your models here.
# Is used to define the properties of the user portfolio and each respective field related to it

# Portfolio model to represent user portfolio data
# *** Placeholder for now
class Portfolio(models.Model):
    user = models.ForeignKey('auth.User', related_name='portfolios', on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=100)
    quantity = models.FloatField()
    purchase_price = models.FloatField()
    current_value = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset_name} - {self.user.username}"