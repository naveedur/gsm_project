from .models import *
import os

def page():
    page=pages.objects.all()
    
    for i in page:
        filepath = os.path.join('firmApp/templates/firmApp/pages', f"{i.title}.html")
        with open(filepath, 'w') as f:
         f.write('oo no')