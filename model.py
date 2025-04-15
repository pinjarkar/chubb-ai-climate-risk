
import requests
from transformers import pipeline
from apscheduler.schedulers.background import BackgroundScheduler

# Define API key and model setup
api_key = 'your_newsapi_key_here'
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

def get_news(api_key, query, language='en'):
    url = f'https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    
    return data['articles']

def summarize_article(article_text):
    summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def classify_article(article_text):
    candidate_labels = ['Climate Risk', 'InsureTech', 'Policies', 'Reinsurance']
    result = classifier(article_text, candidate_labels)
    return result['labels'][0]

def generate_report(article, summary, category, source):
    report = {
        'Headline': article['title'],
        'Category': category,
        'Summary': summary,
        'Business Impact': "Impact of climate risk on insurance market...",
        'Source': source
    }
    return report

def scheduled_scraping():
    print("Scraping news...")
    articles = get_news(api_key, 'climate risk insurance')
    for article in articles:
        summary = summarize_article(article['description'])
        category = classify_article(article['description'])
        report = generate_report(article, summary, category, article['source']['name'])
        print(report)

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_scraping, 'interval', minutes=30)
scheduler.start()
