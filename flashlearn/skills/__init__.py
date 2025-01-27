"""
Initialize the 'skills' subpackage of FlashLearn.

This file ensures 'skills' is recognized as a subpackage.
You can expose certain classes/functions here if desired.
"""

# Example of importing modules or classes:
from .base_skill import BaseSkill
from .classification import ClassificationSkill
from .discover_labels import DiscoverLabelsSkill
from .general_skill import GeneralSkill

__all__ = [
    'BaseSkill',
    'ClassificationSkill',
    'DiscoverLabelsSkill',
    'GeneralSkill',
]