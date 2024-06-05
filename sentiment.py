from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re


tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')

def get_sentiment(news):
    total = 0
    for i in news:
        if i:
            tokens = tokenizer.encode(i, return_tensors = 'pt', padding=True)
            result = model(tokens)
            sentiment = int(torch.argmax(result.logits) + 1)
            total += sentiment
    if total/len(news) < 3:
        return 'negative'
    elif total/len(news) > 3:
            return 'positive'
    return 'neutral'

news = ["Cleveland Fed President Mester Says Fed In 'Really Good Place' To Study Economy Before Deciding Rate Path; Says Not Eager To Consider Interest-Rate Hikes", "Benzinga Closing Bell Update: Indexes Close Higher, Reversing From Premarket Drop, 'Meme Stocks' Soar, Paramount Drops On Reports Sony Is Rethinking Its Bid", 'National Transportation Safety Board Releases Preliminary Report On Baltimore Bridge Collapse', 'TikTok Creators Sue To Block U.S. Divest-Or-Ban Law', "Wall Street Trades Flat On Mixed Producer Inflation; Meme Stocks See Wild Ride, Bitcoin Drops: What's Driving Markets Tuesday?", 'U.S. Relaxes Certain Rules For Government Labs Handling H5N1 Bird Flu To Reduce Burden, Speed Response', "White House Says There's No Need For A Trade War", 'U.S. Trade Rep Tai Says New China Tariffs Designed To Be Strategic Not Chaotic, Effective Not Emotional', "President Biden Says New U.S. Tariffs Are Strategic And Targeted; Former President Trump's Proposed Across-The-Board Tariffs Would Drive Up Costs For Families; I Want Fair Competition With China, Not Conflict; U.S. Standing Up For Peace And Stability Across The Taiwan Strait", "President Biden Says China Heavily Subsidizes Products That Are Dumped On Foreign Markets; We've Seen Damage Here In America; New Tariffs On Chinese Goods Will Ensure Our Workers Are Not Held Back By Unfair Trade Practices; We Will Follow International Trade Laws; U.S. Partners Also Want EV Supply Chain Not Unfairly Dominated By China"]
print(get_sentiment(news))