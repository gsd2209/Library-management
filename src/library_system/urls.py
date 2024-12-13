from django.urls import path, include

urlpatterns = [
    path('api/library/', include('library.urls')),
]
