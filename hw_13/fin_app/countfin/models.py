from django.db import models
from datetime import date

class Сategory(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name

    

class Income(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    amount = models.IntegerField(null=False)
    create_date = models.DateField(default=date.today)
    category_id = models.ForeignKey(Сategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount)

class Spending(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    amount = models.IntegerField(null=False)
    create_date = models.DateField(default=date.today)
    category_id = models.ForeignKey(Сategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount)

