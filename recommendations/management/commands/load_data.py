import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recommendations.models import Book, UserRating
import os

class Command(BaseCommand):
    help = 'Loads book and rating data from Goodreads-10k dataset'

    def handle(self, *args, **options):
        # Path to your CSV files
        books_path = 'goodreads-10k/books.csv'
        ratings_path = 'goodreads-10k/ratings.csv'
        
        # Check if files exist
        if not os.path.exists(books_path) or not os.path.exists(ratings_path):
            self.stdout.write(self.style.ERROR('CSV files not found. Please ensure goodreads-10k/books.csv and goodreads-10k/ratings.csv exist.'))
            return

        self.stdout.write("Loading books data...")
        
        # Load books data
        books_df = pd.read_csv(books_path)
        for _, row in books_df.iterrows():
            Book.objects.get_or_create(
                goodreads_id=row['book_id'],
                defaults={
                    'title': row['title'],
                    'author': row['authors'],
                    'average_rating': row['average_rating']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(books_df)} books"))

        self.stdout.write("Loading ratings data...")
        
        # Load ratings data (using a sample for testing)
        ratings_df = pd.read_csv(ratings_path)
        sample_size = min(10000, len(ratings_df))  # Load max 10k ratings for testing
        ratings_sample = ratings_df.sample(sample_size)
        
        for _, row in ratings_sample.iterrows():
            user, _ = User.objects.get_or_create(username=f"user_{row['user_id']}")
            book = Book.objects.get(goodreads_id=row['book_id'])
            UserRating.objects.get_or_create(
                user=user,
                book=book,
                defaults={'rating': row['rating']}
            )
        
        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(ratings_sample)} ratings"))