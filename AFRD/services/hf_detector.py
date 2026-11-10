import requests
import os


class FakeReviewDetector:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")

        if not self.api_key:
            raise ValueError("HF_API_KEY not found in environment variables.")

        self.API_URL = (
            "https://router.huggingface.co/hf-inference/models/"
            "mrm8488/bert-tiny-finetuned-fake-news-detection"
        )

        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def predict(self, texts):
        """
        texts should be a list of cleaned review strings
        """

        payload = {"inputs": texts}

        response = requests.post(
            self.API_URL,
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()
