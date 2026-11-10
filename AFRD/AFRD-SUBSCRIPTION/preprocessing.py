import re
import string

class TextPreprocessor:
    """
    Handles preprocessing of text data for fake review detection.
    Includes cleaning, normalization, and stop word removal.
    """
    
    def __init__(self, settings=None):
        """
        Initialize the preprocessor with optional settings.
        If settings are not provided, defaults are used.
        """
        self.settings = settings or {
            'remove_stopwords': True,
            'remove_numbers': True,
            'remove_urls': True,
            'lowercase': True
        }
        
        # Common English stop words
        self.stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
            "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 
            'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 
            'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
            'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 
            'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
            'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 
            'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 
            'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 
            'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', 
            "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', 
            "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 
            'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 
            'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
        }

    def clean_text(self, text):
        """
        Performs basic cleaning on the input text based on settings.
        """
        if not text:
            return ""
            
        # Convert to string if not already
        text = str(text)
        
        # Apply lowercase
        if self.settings.get('lowercase', True):
            text = text.lower()
        
        # Remove URLs
        if self.settings.get('remove_urls', True):
            text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove HTML tags (always applied for security/cleanliness)
        text = re.sub(r'<.*?>', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove numbers
        if self.settings.get('remove_numbers', True):
            text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def remove_stopwords(self, text):
        """
        Removes common stop words from the text.
        """
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)

    def process(self, text):
        """
        Main preprocessing pipeline method.
        """
        cleaned_text = self.clean_text(text)
        
        if self.settings.get('remove_stopwords', True):
            cleaned_text = self.remove_stopwords(cleaned_text)
            
        return cleaned_text

# Example usage for testing
if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    sample_review = "This product is amazing! I bought it from http://example.com. 5 stars!!!"
    print(f"Original: {sample_review}")
    print(f"Processed: {preprocessor.process(sample_review)}")