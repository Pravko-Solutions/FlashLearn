"""
Initialize the 'utils' subpackage of FlashLearn.

This file ensures 'utils' is recognized as a subpackage.
You can expose utility classes/functions here if needed.
"""

# Example of importing utility modules or classes:
from .demo_data import imdb_reviews_50k, cats_and_dogs
from .logging_utils import setup_logger
from .token_utils import count_tokens_for_tasks

__all__ = [
    'imdb_reviews_50k', 'cats_and_dogs',
    'setup_logger',
    'count_tokens_for_tasks',
]