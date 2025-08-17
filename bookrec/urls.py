 

# bookrec/urls.py
from django.contrib import admin
from django.urls import path, include
from recommendations.views import home, rate_book, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('rate/<int:book_id>/', rate_book, name='rate_book'),
    
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line
    path('accounts/register/', register, name='register'),  # Custom registration


  ]