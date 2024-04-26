import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')


def load_data(file_path):
    return pd.read_csv(file_path)


def get_tfidf_keywords(reviews, num_keywords=50):  # Consider top 100 keywords
    custom_stop_words = set(stopwords.words('english')).union({'duolingo'})
    tfidf_vectorizer = TfidfVectorizer(stop_words=list(custom_stop_words), max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(reviews)
    feature_array = tfidf_vectorizer.get_feature_names_out()
    tfidf_sorting = tfidf_matrix.toarray().sum(axis=0).argsort()[::-1]

    top_n = feature_array[tfidf_sorting][:num_keywords]
    return top_n, dict(zip(top_n, tfidf_matrix.toarray().sum(axis=0)[tfidf_sorting][:num_keywords]))


def plot_and_save_keyword_distribution(positive_data, negative_data, file_name):
    # Set the keywords as indices and their scores as values
    pos_df = pd.DataFrame(list(positive_data.items()), columns=['Keyword', 'PositiveFrequency'])
    neg_df = pd.DataFrame(list(negative_data.items()), columns=['Keyword', 'NegativeFrequency'])

    # Merge dataframes on keywords to find overlaps
    merged_df = pd.merge(pos_df, neg_df, on='Keyword', how='outer').fillna(0)
    merged_df.set_index('Keyword', inplace=True)

    # Normalize frequencies by the maximum value to scale between 0 and 1
    merged_df['PositiveFrequency'] /= merged_df['PositiveFrequency'].max()
    merged_df['NegativeFrequency'] /= merged_df['NegativeFrequency'].max()

    # Save to CSV
    merged_df.to_csv(file_name)

    # Plotting
    ax = merged_df[['PositiveFrequency', 'NegativeFrequency']].plot(kind='bar', figsize=(14, 7), color=['green', 'red'])
    plt.title('Normalized Frequency of Overlapping Keywords in Positive and Negative Reviews')
    plt.ylabel('Normalized Frequency')
    plt.xlabel('Keywords')
    plt.show()


def main():
    file_path = '/Users/leochen/PycharmProjects/pythonProject8/sentiment_analysis_output.csv'
    output_csv_path = '/Users/leochen/PycharmProjects/pythonProject8/keywords_visual.csv'  # Path where you want to save the CSV
    df = load_data(file_path)

    positive_reviews = df[df['sentiment_type'] == 'positive']['content'].tolist()
    negative_reviews = df[df['sentiment_type'] == 'negative']['content'].tolist()

    positive_keywords, pos_data = get_tfidf_keywords(positive_reviews)
    negative_keywords, neg_data = get_tfidf_keywords(negative_reviews)

    plot_and_save_keyword_distribution(pos_data, neg_data, output_csv_path)


if __name__ == "__main__":
    main()