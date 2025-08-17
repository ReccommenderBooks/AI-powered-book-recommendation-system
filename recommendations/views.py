# from django.shortcuts import render
# # Create your views here.
# # recommendations/views.py
# from django.contrib.auth.decorators import login_required
# from .recommender import BookRecommender

# @login_required
# def home(request):
#     recommender = BookRecommender()
#     recommender.train()
#     recommendations = recommender.recommend_for_user(request.user.id)
    
#     return render(request, 'recommendations/home.html', {
#         'recommendations': recommendations,
#     })

 
# @login_required
# def rate_book(request, book_id):
#     if request.method == 'POST':
#         rating = float(request.POST.get('rating'))
#         UserRating.objects.update_or_create(
#             user=request.user,
#             book_id=book_id,
#             defaults={'rating': rating}
#         )
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error'}, status=400)


# recommendations/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Book, UserRating
from .recommender import BookRecommender

def home(request):
    recommender = BookRecommender()
    recommender.train()
    recommendations = recommender.recommend_for_user(request.user.id) if request.user.is_authenticated else []
    return render(request, 'recommendations/home.html', {'recommendations': recommendations})

def rate_book(request, book_id):
    if request.method == 'POST':
        rating = float(request.POST.get('rating'))
        UserRating.objects.update_or_create(
            user=request.user,
            book_id=book_id,
            defaults={'rating': rating}
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

 

# recommendations/views.py
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})