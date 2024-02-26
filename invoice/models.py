from django.db import models

# Create your models here.
class extractApp(models.Model):
    content = models.TextField()

class pdf(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pdf = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title