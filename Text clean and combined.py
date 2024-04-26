import pandas as pd
import re
from langdetect import detect, LangDetectException


def remove_emojis(text):
    # Regex to match typical emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F700-\U0001F77F"  # alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U00002702-\U000027B0"  # Dingbats
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def clean_reviews(input_file):
    # Load data
    df = pd.read_csv(input_file)

    # Remove blank content
    df.dropna(subset=['content'], inplace=True)

    # Remove emojis and numbers from content
    df['content'] = df['content'].apply(remove_emojis)
    df['content'] = df['content'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))

    # Remove rows where content is only whitespace or empty after cleaning
    df = df[df['content'].str.strip().astype(bool)]

    # Remove duplicate content
    df.drop_duplicates(subset=['content'], inplace=True)

    # Remove non-English content
    df = df[df['content'].apply(is_english)]

    # Remove content with less than two words
    df = df[df['content'].apply(lambda x: len(x.split()) >= 2)]

    return df


def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False


def combine_and_save_dfs(df1, df2, output_file):
    # Combine dataframes
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Save the combined data
    combined_df.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file}")


if __name__ == "__main__":
    # Path to the input CSV files
    input_file_google = '/Users/leochen/PycharmProjects/pythonProject8/duolingo_reviews_google.csv'
    input_file_apple = '/Users/leochen/PycharmProjects/pythonProject8/duolingo_reviews_apple.csv'

    # Path for the output combined CSV file
    output_file_combined = '/Users/leochen/PycharmProjects/pythonProject8/combined_Duo_reviews.csv'

    # Clean Google Play reviews
    cleaned_google_reviews = clean_reviews(input_file_google)

    # Clean Apple Store reviews
    cleaned_apple_reviews = clean_reviews(input_file_apple)

    # Combine and save the cleaned reviews into one file
    combine_and_save_dfs(cleaned_google_reviews, cleaned_apple_reviews, output_file_combined)