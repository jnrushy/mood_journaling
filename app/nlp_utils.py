"""
Natural Language Processing utilities for mood analysis.

This module provides functions to analyze journal entries and extract mood-related insights
using TextBlob for sentiment analysis and basic text processing.
"""

import re
from typing import Dict, List, Tuple, Optional
from textblob import TextBlob
import pandas as pd


def analyze_sentiment(text: str) -> float:
    """
    Analyze the sentiment of a given text using TextBlob.
    
    TextBlob uses a rule-based approach to determine sentiment polarity:
    - Returns a value between -1 (very negative) and +1 (very positive)
    - 0 indicates neutral sentiment
    
    Args:
        text (str): The text to analyze (journal entry content)
        
    Returns:
        float: Sentiment polarity score between -1 and 1
    """
    # Create a TextBlob object from the input text
    blob = TextBlob(text)
    
    # Extract the sentiment polarity (how positive/negative the text is)
    # This is based on predefined sentiment lexicons and rules
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def categorize_mood(sentiment_score: float) -> str:
    """
    Categorize a sentiment score into a human-readable mood label.
    
    This function takes the numerical sentiment score and converts it into
    a categorical mood that's easier to understand and visualize.
    
    Args:
        sentiment_score (float): Sentiment polarity from -1 to 1
        
    Returns:
        str: Mood category ('Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive')
    """
    if sentiment_score <= -0.5:
        return "Very Negative"
    elif sentiment_score <= -0.1:
        return "Negative"
    elif sentiment_score <= 0.1:
        return "Neutral"
    elif sentiment_score <= 0.5:
        return "Positive"
    else:
        return "Very Positive"


def extract_keywords(text: str, min_length: int = 4, max_words: int = 50) -> List[str]:
    """
    Extract meaningful keywords from text for word cloud generation.
    
    This function cleans the text, removes common stop words, and extracts
    words that are likely to be meaningful for mood analysis.
    
    Args:
        text (str): The text to extract keywords from
        min_length (int): Minimum word length to include (filters out short words)
        max_words (int): Maximum number of words to return
        
    Returns:
        List[str]: List of cleaned keywords
    """
    # Convert to lowercase and split into words
    words = text.lower().split()
    
    # A more comprehensive list of English stop words
    stop_words = {
        'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at',
        'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
        'can', 'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each',
        'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself',
        'him', 'himself', 'his', 'how', 'if', 'in', 'into', 'is', 'it', 'its', 'itself',
        'just', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once',
        'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so',
        'some', 'still', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
        'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we',
        'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would',
        'you', 'your', 'yours', 'yourself', 'yourselves', 'like', 'im', 'ive', 'also', 'get', 'got'
    }
    
    # Clean and filter words
    cleaned_words = []
    for word in words:
        # Remove punctuation and numbers
        clean_word = re.sub(r'[^a-zA-Z]', '', word)
        
        # Only include words that meet our criteria
        if (len(clean_word) >= min_length and 
            clean_word not in stop_words and 
            clean_word.isalpha()):
            cleaned_words.append(clean_word)
    
    # Return the most frequent words (up to max_words)
    return cleaned_words[:max_words]


def analyze_journal_entries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze a dataframe of journal entries and add sentiment analysis columns.
    
    This is the main function that processes your journal data. It takes your
    raw journal entries and adds sentiment scores, mood categories, and keywords.
    
    Args:
        df (pd.DataFrame): DataFrame with columns 'date', 'title', 'content'
        
    Returns:
        pd.DataFrame: Original dataframe with added columns:
            - sentiment_score: Numerical sentiment (-1 to 1)
            - subjectivity_score: Numerical subjectivity (0 to 1)
            - mood_category: Categorical mood label
            - keywords: List of extracted keywords
    """
    # Create a copy to avoid modifying the original dataframe
    processed_df = df.copy()
    
    # Add sentiment analysis columns
    sentiments = processed_df['content'].apply(lambda text: analyze_sentiment(text))
    processed_df['sentiment_score'] = sentiments.apply(lambda x: x[0])
    processed_df['subjectivity_score'] = sentiments.apply(lambda x: x[1])
    processed_df['mood_category'] = processed_df['sentiment_score'].apply(categorize_mood)
    
    # Extract keywords from content
    processed_df['keywords'] = processed_df['content'].apply(extract_keywords)
    
    # Convert date column to datetime if it's not already
    if 'date' in processed_df.columns:
        processed_df['date'] = pd.to_datetime(processed_df['date'])
    
    return processed_df


def get_mood_statistics(df: pd.DataFrame) -> tuple:
    """
    Calculate summary statistics for the dashboard display.
    
    Args:
        df (pd.DataFrame): Processed dataframe with sentiment analysis
        
    Returns:
        tuple: A tuple containing:
            - total_entries (int)
            - avg_mood (float)
            - most_common_mood (str)
            - date_range (int)
    """
    if df.empty:
        return 0, 0.0, "N/A", 0
        
    total_entries = len(df)
    avg_mood = df['sentiment_score'].mean()
    most_common_mood = df['mood_category'].mode().iloc[0] if not df.empty else "N/A"
    
    # Calculate date range in days
    if 'date' in df.columns and not df['date'].empty:
        date_range = (df['date'].max() - df['date'].min()).days
    else:
        date_range = 0
        
    return total_entries, avg_mood, most_common_mood, date_range


def get_common_keywords(df: pd.DataFrame, top_n: int = 20) -> List[Tuple[str, int]]:
    """
    Find the most common keywords across all journal entries.
    
    This function aggregates keywords from all entries and returns the most
    frequently occurring ones, which can help identify recurring themes.
    
    Args:
        df (pd.DataFrame): Processed dataframe with keywords column
        top_n (int): Number of top keywords to return
        
    Returns:
        List[Tuple[str, int]]: List of (keyword, frequency) tuples
    """
    # Flatten all keywords into a single list
    all_keywords = []
    for keywords in df['keywords']:
        all_keywords.extend(keywords)
    
    # Count keyword frequencies
    keyword_counts = {}
    for keyword in all_keywords:
        keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    
    # Sort by frequency and return top N
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_keywords[:top_n] 