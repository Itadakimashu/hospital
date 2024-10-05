import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from doctor.models import Doctor

class Command(BaseCommand):
    help = 'Download random images from the internet and assign them to doctors'

    def handle(self, *args, **kwargs):
        # List of random image URLs (You can replace these with any valid image URLs)
        image_urls = [
            'https://randomuser.me/api/portraits/men/1.jpg',
            'https://randomuser.me/api/portraits/women/1.jpg',
            'https://randomuser.me/api/portraits/men/2.jpg',
            'https://randomuser.me/api/portraits/women/2.jpg',
            'https://randomuser.me/api/portraits/men/3.jpg',
            'https://randomuser.me/api/portraits/women/3.jpg'
        ]

        # Loop through all doctors and assign a random image
        doctors = Doctor.objects.all()
        for doctor in doctors:
            # Choose a random image URL
            image_url = image_urls[doctor.id % len(image_urls)]  # Modulo to cycle through the images

            # Fetch the image from the internet
            response = requests.get(image_url)
            if response.status_code == 200:
                # Remove 'delete=True'
                img_temp = NamedTemporaryFile()
                img_temp.write(response.content)
                img_temp.flush()

                # Assign the downloaded image to the doctor's image field
                doctor.image.save(f"{doctor.user.username}_profile.jpg", File(img_temp))
                doctor.save()

                self.stdout.write(self.style.SUCCESS(f"Assigned image to Dr. {doctor.user.first_name} {doctor.user.last_name}"))

        self.stdout.write(self.style.SUCCESS('Successfully downloaded and assigned images to all doctors!'))
