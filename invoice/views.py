import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image

from .models import pdf

def home(request):
    pdfs = pdf.objects.all()
    return render(request, 'home.html', {
        'pdfs': pdfs
    })

def upload(request):
    context = {}
    
    # Configure Tesseract OCR path for macOS
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

    if request.method == 'POST':
        upload_file = request.FILES['document']

        # Upload file to server
        fs =  FileSystemStorage()
        name = fs.save(upload_file.name, upload_file)
        context['url'] = fs.url(name)

        # Extract text from pdf
        pdfFileObj = open(os.path.join(fs.base_location, upload_file.name), 'rb')
        pdf_read = PdfReader(pdfFileObj)
        text = ""
        for page in pdf_read.pages:
            page_images = page.images
            for image in page_images:
                image_data = image.data
                with open("image.jpg", "wb") as f:
                    f.write(image_data)

                    image = Image.open("image.jpg")
                    text += pytesseract.image_to_string(image)
                    f.close()
                    os.remove("image.jpg") 

        print("Content of PDF: ----> " + text)

        # Save PDF details to database
        pdf.objects.create(title=name, content=text, pdf=context['url'])
        
    return render(request, 'upload.html', context)
