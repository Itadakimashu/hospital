from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from doctor.models import Doctor, Specialization, AvailableTime, Designation
from random import choice
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generate dummy data for doctors, specializations, available times, and designations'

    def handle(self, *args, **kwargs):
        # Create some Designations
        designations = ['Cardiologist', 'Neurologist', 'Pediatrician', 'General Physician', 'Dermatologist']
        designation_objs = []
        for name in designations:
            designation, created = Designation.objects.get_or_create(
                name=name,
                slug=fake.slug(name)
            )
            designation_objs.append(designation)

        # Create some Specializations
        specializations = ['Cardiology', 'Neurology', 'Pediatrics', 'General Medicine', 'Dermatology']
        specialization_objs = []
        for name in specializations:
            specialization, created = Specialization.objects.get_or_create(
                name=name,
                slug=fake.slug(name)
            )
            specialization_objs.append(specialization)

        # Create AvailableTime slots
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        available_time_objs = []
        for _ in range(5):
            available_time = AvailableTime.objects.create(
                from_day=choice(days_of_week),
                to_day=choice(days_of_week),
                start_time=fake.time(),
                end_time=fake.time()
            )
            available_time_objs.append(available_time)

        # Create dummy Users and Doctors
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password='password123'
            )
            
            # Create Doctor
            doctor = Doctor.objects.create(
                user=user,
                image=fake.image_url(),
                designation=choice(designation_objs),
                fee=round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2),
                meet_link=fake.url()
            )

            # Add specializations and available times to the doctor
            doctor.specialization.set(specialization_objs)
            doctor.available_time.set(available_time_objs)

            doctor.save()

        self.stdout.write(self.style.SUCCESS('Successfully created dummy data!'))
    