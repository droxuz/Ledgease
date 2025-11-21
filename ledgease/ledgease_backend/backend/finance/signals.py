from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, UserFinanceData

# Signal to update UserFinanceData after a Transaction is saved
@receiver(post_save, sender=Transaction)
def update_finance_data_on_save(sender, instance, **kwargs):
    finance_data, created = UserFinanceData.objects.get_or_create(user=instance.user)
    finance_data.CalculateTotals()

# Signal to update UserFinanceData after a Transaction is deleted
@receiver(post_delete, sender=Transaction)
def update_finance_data_on_delete(sender, instance, **kwargs):
    finance_data, created = UserFinanceData.objects.get_or_create(user=instance.user)
    finance_data.CalculateTotals()