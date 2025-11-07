from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.name

class Bill(models.Model):
    patient_name = models.CharField(max_length=100)
    medicines = models.ManyToManyField('Medicine', through='BillItem')
    amount_paid = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.date.strftime('%Y-%m-%d')}"

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity} for {self.bill.patient_name}"
