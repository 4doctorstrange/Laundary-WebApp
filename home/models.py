from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100)
    block = models.CharField(max_length=2)
    room_no = models.IntegerField()
    cycles_remaining = models.IntegerField(default=3)

    def __str__(self):
        return self.user


class UseCycle(models.Model):
    cloth = [
        ('1-5', (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))),
        ('6-10', (('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'))),
        ('11-15', (('11', '11'), ('12', '12'),
                   ('13', '13'), ('14', '14'), ('15', '15'))),
        ('16-20', (('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20')))
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    no_of_clothes = models.CharField(max_length=6, choices=cloth)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    delivery_date = models.DateField()
    collection_info = models.DateTimeField(null=True)
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.student