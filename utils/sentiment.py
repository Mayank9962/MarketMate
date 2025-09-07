from transformers import pipeline 
 
def analyze_sentiment(text: str): 
    """ 
    Uses HuggingFace's pre-trained sentiment analysis model. 
    """ 
    # Use a pre-trained sentiment analysis pipeline 
    try: 
        classifier = pipeline("sentiment-analysis") 
        result = classifier(text) 
         
        label = result[0]['label'] 
        score = result[0]['score'] 
         
        if label == "POSITIVE" and score > 0.85: 
            return "Positive" 
        elif label == "NEGATIVE" and score > 0.85: 
            return "Negative" 
        else: 
            return "Mixed" 
             
    except Exception as e: 
        print(f"Sentiment analysis failed: {e}") 
        return "Mixed" 