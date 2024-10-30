import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def plot_orientation_distribution(df):
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='orientation')
    plt.title('Tweet Orientation Distribution')
    plt.xlabel('Orientation')
    plt.ylabel('Count')
    plt.show()


def plot_average_engagement(df):
    avg_engagement = df.groupby('orientation').agg({
        'likes': 'mean',
        'retweets': 'mean',
        'replies': 'mean'
    }).reset_index()

    plt.figure(figsize=(10, 5))
    avg_engagement.plot(x='orientation', kind='bar', stacked=True)
    plt.title('Average Engagement by Tweet Orientation')
    plt.ylabel('Average Counts')
    plt.xticks(rotation=45)
    plt.show()


def plot_tweet_volume_over_time(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    plt.figure(figsize=(12, 6))
    df.resample('D').size().plot()
    plt.title('Tweet Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Tweets')
    plt.show()


def plot_orientation_over_time(df):
    orientation_over_time = df.groupby([df.index.date, 'orientation']).size().unstack(fill_value=0)
    orientation_over_time.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.title('Tweet Orientation Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Tweets')
    plt.xticks(rotation=45)
    plt.show()


def plot_word_clouds(df):
    for orientation in df['orientation'].unique():
        text = ' '.join(df[df['orientation'] == orientation]['content'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud for {orientation} Tweets')
        plt.show()


def plot_engagement_correlation(df):
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[['likes', 'retweets', 'replies']].corr(), annot=True, cmap='coolwarm')
    plt.title('Engagement Metrics Correlation')
    plt.show()


def analyze_posts_data(df):
    plot_orientation_distribution(df)
    plot_average_engagement(df)
    plot_tweet_volume_over_time(df)
    plot_orientation_over_time(df)
    plot_word_clouds(df)
    plot_engagement_correlation(df)
