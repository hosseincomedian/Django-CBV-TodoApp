from django.shortcuts import render, redirect
from django.views.static import serve
import time
def test(request, path):
    # time.sleep(5)
    # http://localhost/media/photo/Snake_img.png
    path = "Snake_img.png"
    print(path)
    response = serve(request, path, document_root='media/photo/')
    print("response:")
    response['Cache-Control'] = 'public, max-age=86400'  # Set caching headers for 1 day
    response['X-Custom-Header'] = 'Custom value'  # Set custom header
    # return redirect("http://localhost/media/photo/Snake_img.png")
    print(response)
    return response
