from django.db import models

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class District(models.Model):
    state = models.ForeignKey(State)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    capital = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Taluk(models.Model):
    district = models.ForeignKey(District)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


#Bank databse
class BankType(models.Model):
    name = models.CharField(max_length=20)


class Bank(models.Model):
    bank_name = models.CharField(max_length=50)
    bank_type = models.ForeignKey(BankType)

    def __str__(self):
        return self.bank_name

class BankBranch(models.Model):
    district = models.ForeignKey(District)
    bank = models.ForeignKey(Bank)
    branch_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=100)
    state = models.ForeignKey(State)
    taluk = models.ForeignKey(Taluk, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    micr_code = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.branch_name