import pytest

from flashlearn.utils.demo_data import cats_and_dogs, imdb_reviews_50k


@pytest.mark.parametrize("sample,train_ratio", [
    (10, 0.5),
    (20, 0.2),
])
def test_cats_and_dogs(sample, train_ratio):
    """
    Test that cats_and_dogs runs end-to-end, downloads the dataset,
    and returns lists of dictionaries with the correct keys.
    """
    test_data = cats_and_dogs(sample=sample, train_ratio=train_ratio)

    # Check type
    assert isinstance(test_data, list), "test_data should be a list."

    # Check lengths roughly match the ratio
    total_len = len(test_data)
    assert total_len == sample, f"Total returned items must be equal to sample={sample}"

    # Check at least one item if sample > 0
    if sample > 0:
        assert len(test_data) > 0, "Expected some testing data."

        # Check structure of first item
        first_item = test_data[0]
        assert "image_base64" in first_item, "Each item should have 'image_base64'."
        assert "label" in first_item, "Each item should have 'label'."
        assert isinstance(first_item["image_base64"], str), "'image_base64' must be a string."
        assert isinstance(first_item["label"], int), "'label' must be an integer."


@pytest.mark.parametrize("sample", [10, 20])
def test_imdb_reviews_50k(sample):
    """
    Test that imdb_reviews_50k runs end-to-end, downloads the IMDb dataset,
    randomly samples the requested number of rows, and splits them.
    """
    test_data = imdb_reviews_50k(sample=sample)

    # Basic checks
    assert isinstance(test_data, list), "test_data should be a list."
    total_len = len(test_data)
    assert total_len == sample, f"Total returned items must match requested sample={sample}."

    # Check keys
    if sample > 0:
        first_item = test_data[0]
        assert "review" in first_item, "Should contain a 'review' field."
        assert "sentiment" in first_item, "Should contain a 'sentiment' field."
        assert isinstance(first_item["review"], str), "'review' must be a string."
        assert isinstance(first_item["sentiment"], str), "'sentiment' must be a string."