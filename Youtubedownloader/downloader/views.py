from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.conf import settings
import yt_dlp
import os

SAVE_PATH = os.path.join(settings.BASE_DIR, 'downloads')


if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

def index(request):
    return render(request, 'index.html')

def download(request):
    if request.method == 'POST':
        url = request.POST['url']
        path = request.POST['path']
        download_status = False

        try:
            if not os.path.exists(path):
                os.makedirs(path)

            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            download_status = True
        except Exception as e:
            return render(request, 'index.html', {'error': str(e)})

        return render(request, 'index.html', {'download_status': download_status})

    return redirect('index')