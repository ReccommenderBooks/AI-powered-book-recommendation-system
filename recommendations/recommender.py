# # recommendations/recommender.py
# from surprise import Dataset, Reader, SVD
# from surprise.model_selection import train_test_split
# from recommendations.models import UserRating
# import pandas as pd
# import numpy as np

# class BookRecommender:
#     def __init__(self):
#         self.model = SVD()  # Matrix factorization algorithm
#         self.trainset = None

#     def load_data(self):
#         """Load ratings data into Surprise format"""
#         ratings = UserRating.objects.all().values('user_id', 'book_id', 'rating')
#         df = pd.DataFrame(list(ratings))
#         reader = Reader(rating_scale=(1, 5))
#         data = Dataset.load_from_df(df[['user_id', 'book_id', 'rating']], reader)
#         self.trainset = data.build_full_trainset()

#     def train(self):
#         """Train the model"""
#         if not self.trainset:
#             self.load_data()
#         self.model.fit(self.trainset)

#     def recommend_for_user(self, user_id, n=5):
#         """Generate top N recommendations for a user"""
#         if not self.trainset:
#             self.load_data()
        
#         # Get all books the user hasn't rated
#         rated_books = set(UserRating.objects.filter(user_id=user_id).values_list('book_id', flat=True))
#         all_books = Book.objects.exclude(id__in=rated_books)
        
#         # Predict ratings for unrated books
#         predictions = []
#         for book in all_books:
#             pred = self.model.predict(user_id, book.id)
#             predictions.append((book, pred.est))
        
#         # Return top N highest predicted ratings
#         predictions.sort(key=lambda x: x[1], reverse=True)
#         return [book for book, _ in predictions[:n]]

 

        #######################################################

import numpy as np
from collections import defaultdict
from django.db.models import Avg
from recommendations.models import UserRating, Book

class BookRecommender:
    def __init__(self):
        self.user_ratings = None
        self.book_means = None
        self.user_means = None
        self.trainset = None  # Added for compatibility
        self.model = self  # Added for compatibility
        
    def load_data(self):
        """Load ratings data into memory"""
        ratings = UserRating.objects.all().values('user_id', 'book_id', 'rating')
        self.user_ratings = defaultdict(dict)
        self.book_means = defaultdict(float)
        self.user_means = defaultdict(float)
        
        # Store individual ratings and calculate means
        book_ratings = defaultdict(list)
        user_ratings = defaultdict(list)
        
        for rating in ratings:
            user_id = rating['user_id']
            book_id = rating['book_id']
            rating_val = rating['rating']
            
            self.user_ratings[user_id][book_id] = rating_val
            book_ratings[book_id].append(rating_val)
            user_ratings[user_id].append(rating_val)
        
        # Calculate mean ratings
        for book_id, ratings in book_ratings.items():
            self.book_means[book_id] = np.mean(ratings)
        
        for user_id, ratings in user_ratings.items():
            self.user_means[user_id] = np.mean(ratings)
        
        self.global_mean = np.mean(list(self.book_means.values())) if self.book_means else 3.0
        self.trainset = True  # Mark as loaded

    def train(self):
        """Compatibility method - data is already loaded and processed in load_data()"""
        if not self.trainset:
            self.load_data()
        return self

    def recommend_for_user(self, user_id, n=5):
        """Generate recommendations using weighted scoring"""
        if not self.trainset:
            self.load_data().train()
            
        # Get books the user hasn't rated
        rated_books = set(self.user_ratings.get(user_id, {}).keys())
        unrated_books = Book.objects.exclude(id__in=rated_books)
        
        # Calculate user average (fall back to global mean if no ratings)
        user_avg = self.user_means.get(user_id, self.global_mean)
        
        # Score unrated books
        recommendations = []
        for book in unrated_books:
            book_avg = self.book_means.get(book.id, self.global_mean)
            # Hybrid score: 60% book quality + 40% user preference
            score = 0.6 * book_avg + 0.4 * user_avg
            recommendations.append((book, score))
        
        # Return top N recommendations
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [book for book, _ in recommendations[:n]]