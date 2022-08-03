from django.core.files.uploadedfile import InMemoryUploadedFile
import base64,re,sys, datetime
from PIL import Image
from io import BytesIO
from rest_framework import serializers

def base64ToImage(base64_image_data):
    try:
        buffer_plot = BytesIO()
        base64_data = re.sub('^data:image/.+;base64,', '', base64_image_data)
        binary_data = base64.b64decode(base64_data)
        img_data = BytesIO(binary_data)
        img = Image.open(img_data)
        try:
            img.save(buffer_plot, format='PNG', quality=100)
        except:
            img.save(buffer_plot, format='JPEG', quality=100)
        buffer_plot.seek(0)
        return InMemoryUploadedFile(buffer_plot, 'ImageField',f'''{datetime.datetime.now().strftime("%d%m%y%H%M%S%f")}.png''','image/png',sys.getsizeof(buffer_plot), None)
    except Exception as e:
        raise serializers.ValidationError({"image":f"{e}"})
