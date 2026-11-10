import re

class TextPreprocessor:
    def __init__(self, reviews):
        """
        reviews: list of review strings
        """
        self.reviews = reviews

    def preprocess(self):
        cleaned_reviews = []

        for text in self.reviews:
            text = text.lower()
            text = re.sub(r"http\S+", "", text)
            text = re.sub(r"[^a-z\s]", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            cleaned_reviews.append(text)

        return cleaned_reviews