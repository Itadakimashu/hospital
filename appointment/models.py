from django.db import models

from doctor.models import Doctor,AvailableTime
from paitent.models import Paitent
# Create your models here.

appointment_status = [
    ('pending','pending'),
    ('running','running'),
    ('cancelled','cancelled'),
    ('completed','completed'),
    ]

appointment_type = [
    ('Online','Online'),
    ('Offline','Offline'),
]

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    paitent = models.ForeignKey(Paitent,on_delete=models.CASCADE,related_name='appointments')
    time = models.ForeignKey(AvailableTime,on_delete=models.CASCADE)
    symptoms = models.TextField()
    type = models.CharField(choices=appointment_type,max_length=15)
    status = models.CharField(choices=appointment_status,default='pending',max_length=15)
    doctor_review = models.TextField(blank=True)

    def __str__(self):
        return f'Paitent: {self.paitent} | Doctor: {self.doctor} | Time : {self.time}'