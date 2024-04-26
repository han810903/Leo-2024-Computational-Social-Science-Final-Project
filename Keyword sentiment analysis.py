import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import nltk

# Ensure necessary NLTK resources are downloaded
nltk.download('vader_lexicon')

# Load the dataset
df = pd.read_csv('/Users/leochen/PycharmProjects/pythonProject8/combined_Duo_reviews.csv')

# Initialize sentiment analysis tool
sia = SentimentIntensityAnalyzer()

# Define specific aspects you want to focus on
focus_keywords = ['feedback', 'interaction', 'grammar', 'language', 'vocabulary', 'streak', 'rewards', 'pronunciation', 'speaking', 'practice', 'exercises', 'games']

# Analyze sentiment and check for the presence of focus keywords
def analyze_sentiment(row):
    sentence = row['content']
    sentiment = sia.polarity_scores(sentence)
    row['compound'] = sentiment['compound']
    for keyword in focus_keywords:
        if keyword in sentence.lower():
            row[keyword] = sentiment['compound']
    return row

# Apply the function to the dataframe
df = df.apply(analyze_sentiment, axis=1)

# Aggregate the sentiment scores for reviews containing each keyword
keyword_sentiment = {keyword: df[keyword].mean() for keyword in focus_keywords if keyword in df.columns}

# Save the keyword sentiment data to a CSV file
keyword_sentiment_df = pd.DataFrame(list(keyword_sentiment.items()), columns=['Keyword', 'Average Sentiment'])
keyword_sentiment_df.to_csv('/Users/leochen/PycharmProjects/pythonProject8/focused_keywords_sentiment.csv', index=False)

# Visualization of keyword sentiment
plt.figure(figsize=(10, 5))
plt.bar(keyword_sentiment_df['Keyword'], keyword_sentiment_df['Average Sentiment'], color='blue')
plt.title('Average Sentiment Score for Duolingo Reviews by Keyword')
plt.xlabel('Keywords')
plt.ylabel('Average Sentiment Score')
plt.ylim(-1, 1)  # Sentiment scores range from -1 to 1
plt.axhline(0, color='grey', linewidth=0.8)  # This line represents the neutral sentiment score
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/Users/leochen/PycharmProjects/pythonProject8/focused_keywords_plot.png')
plt.close()