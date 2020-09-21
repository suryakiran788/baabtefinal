from django.db import models
from django import forms
# Create your models here.

class Department(models.Model):
    dept_name=models.CharField(max_length=30)
    dept_id=models.IntegerField()

class Batch(models.Model):
    name=models.CharField(max_length=30, unique=True, null=False)
    department=models.CharField(max_length=30)

class Users(models.Model):
    username=models.BigIntegerField()
    password=models.CharField(max_length=30)
    role=models.CharField(max_length=30)


class Student(models.Model):
    name=models.CharField(max_length=30)
    # std_id=models.ForeignKey(Users, on_delete=models.CASCADE, primary_key=True)
    std_id=models.ForeignKey(Users,on_delete=models.CASCADE)
    department=models.CharField(max_length=30)
    dateofbirth=models.DateField(blank=True, null=True) 
    blood_group=models.CharField(max_length=5)
    phone=models.BigIntegerField()
    dateofjoin=models.DateField(blank=True, null=True)
    batch=models.CharField(max_length=20)
    designation=models.CharField(max_length=30)
    image=models.CharField(max_length=50)

class Staff(models.Model):
    name=models.CharField(max_length=30)
    std_id=models.ForeignKey(Users, on_delete=models.CASCADE)
    department=models.CharField(max_length=30)
    dateofbirth=models.DateField(blank=True, null=True) 
    blood_group=models.CharField(max_length=5)
    phone=models.BigIntegerField()
    dateofjoin=models.DateField(blank=True, null=True)
    designation=models.CharField(max_length=30)
    image=models.CharField(max_length=50)
    sectionincharge=models.CharField(max_length=20, default='no')


class Admin(models.Model):
    username=models.CharField(max_length=40)
    password=models.CharField(max_length=30)
# (input_formats=DATE_INPUT_FORMATS) 





    

 