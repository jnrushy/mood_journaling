"""
Database utilities for storing and retrieving journal entry data.

This module handles all database operations using SQLite, including creating tables,
inserting processed journal entries, and querying data for the dashboard.
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path


class JournalDatabase:
    """
    A class to handle all database operations for the mood journaling app.
    
    This class provides methods to:
    - Initialize the database and create tables
    - Store processed journal entries
    - Query entries with various filters
    - Get aggregated statistics
    """
    
    def __init__(self, db_path: str = "data/journal_mood.db"):
        """
        Initialize the database connection and create tables if they don't exist.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        # Ensure the data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.conn = None
        self._create_tables()
    
    def _create_tables(self):
        """
        Create the necessary database tables if they don't exist.
        
        This method creates a table structure that can store:
        - Basic journal entry information (date, title, content)
        - Sentiment analysis results (sentiment_score, mood_category)
        - Keywords extracted from entries
        """
        try:
            # Connect to the database (creates it if it doesn't exist)
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create the main journal entries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    sentiment_score REAL,
                    mood_category TEXT,
                    keywords TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create an index on the date column for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_date ON journal_entries(date)
            ''')
            
            # Create an index on sentiment_score for mood filtering
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_sentiment ON journal_entries(sentiment_score)
            ''')
            
            self.conn.commit()
            print(f"Database initialized at {self.db_path}")
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
    
    def insert_entries(self, df: pd.DataFrame) -> int:
        """
        Insert processed journal entries into the database.
        
        This method takes a DataFrame with sentiment analysis results and
        stores them in the database for later retrieval and analysis.
        
        Args:
            df (pd.DataFrame): DataFrame with columns: date, title, content, 
                              sentiment_score, mood_category, keywords
                              
        Returns:
            int: Number of entries successfully inserted
        """
        if self.conn is None:
            self._create_tables()
        
        cursor = self.conn.cursor()
        inserted_count = 0
        
        try:
            # Prepare the data for insertion
            for _, row in df.iterrows():
                # Convert keywords list to string for storage
                keywords_str = ','.join(row.get('keywords', [])) if row.get('keywords') else ''
                
                cursor.execute('''
                    INSERT INTO journal_entries 
                    (date, title, content, sentiment_score, mood_category, keywords)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    str(row['date']),
                    row.get('title', ''),
                    row['content'],
                    row.get('sentiment_score', 0.0),
                    row.get('mood_category', 'Neutral'),
                    keywords_str
                ))
                inserted_count += 1
            
            self.conn.commit()
            print(f"Successfully inserted {inserted_count} entries")
            
        except sqlite3.Error as e:
            print(f"Error inserting entries: {e}")
            self.conn.rollback()
            raise
        
        return inserted_count
    
    def get_all_entries(self) -> pd.DataFrame:
        """
        Retrieve all journal entries from the database.
        
        Returns:
            pd.DataFrame: DataFrame with all journal entries and their analysis
        """
        if self.conn is None:
            self._create_tables()
        
        query = '''
            SELECT date, title, content, sentiment_score, mood_category, keywords
            FROM journal_entries
            ORDER BY date DESC
        '''
        
        df = pd.read_sql_query(query, self.conn)
        
        # Convert date strings back to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Convert keywords string back to list
        df['keywords'] = df['keywords'].apply(
            lambda x: x.split(',') if x else []
        )
        
        return df
    
    def get_entries_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Retrieve journal entries within a specific date range.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            pd.DataFrame: Filtered entries within the date range
        """
        if self.conn is None:
            self._create_tables()
        
        query = '''
            SELECT date, title, content, sentiment_score, mood_category, keywords
            FROM journal_entries
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC
        '''
        
        df = pd.read_sql_query(query, self.conn, params=[start_date, end_date])
        
        # Convert date strings back to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Convert keywords string back to list
        df['keywords'] = df['keywords'].apply(
            lambda x: x.split(',') if x else []
        )
        
        return df
    
    def get_entries_by_mood(self, mood_category: str) -> pd.DataFrame:
        """
        Retrieve journal entries with a specific mood category.
        
        Args:
            mood_category (str): Mood category to filter by
            
        Returns:
            pd.DataFrame: Entries with the specified mood
        """
        if self.conn is None:
            self._create_tables()
        
        query = '''
            SELECT date, title, content, sentiment_score, mood_category, keywords
            FROM journal_entries
            WHERE mood_category = ?
            ORDER BY date DESC
        '''
        
        df = pd.read_sql_query(query, self.conn, params=[mood_category])
        
        # Convert date strings back to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Convert keywords string back to list
        df['keywords'] = df['keywords'].apply(
            lambda x: x.split(',') if x else []
        )
        
        return df
    
    def search_entries(self, search_term: str) -> pd.DataFrame:
        """
        Search journal entries by content or title.
        
        Args:
            search_term (str): Text to search for in entries
            
        Returns:
            pd.DataFrame: Entries containing the search term
        """
        if self.conn is None:
            self._create_tables()
        
        query = '''
            SELECT date, title, content, sentiment_score, mood_category, keywords
            FROM journal_entries
            WHERE content LIKE ? OR title LIKE ?
            ORDER BY date DESC
        '''
        
        search_pattern = f'%{search_term}%'
        df = pd.read_sql_query(query, self.conn, params=[search_pattern, search_pattern])
        
        # Convert date strings back to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Convert keywords string back to list
        df['keywords'] = df['keywords'].apply(
            lambda x: x.split(',') if x else []
        )
        
        return df
    
    def get_mood_statistics(self) -> Dict:
        """
        Get aggregated mood statistics from the database.
        
        Returns:
            Dict: Dictionary containing mood statistics
        """
        if self.conn is None:
            self._create_tables()
        
        stats = {}
        
        # Get basic counts
        cursor = self.conn.cursor()
        
        # Total entries
        cursor.execute('SELECT COUNT(*) FROM journal_entries')
        stats['total_entries'] = cursor.fetchone()[0]
        
        # Average sentiment
        cursor.execute('SELECT AVG(sentiment_score) FROM journal_entries')
        stats['average_sentiment'] = cursor.fetchone()[0] or 0.0
        
        # Mood distribution
        cursor.execute('''
            SELECT mood_category, COUNT(*) 
            FROM journal_entries 
            GROUP BY mood_category
        ''')
        mood_counts = dict(cursor.fetchall())
        stats['mood_distribution'] = mood_counts
        
        # Monthly sentiment averages
        cursor.execute('''
            SELECT strftime('%Y-%m', date) as month, AVG(sentiment_score)
            FROM journal_entries
            GROUP BY month
            ORDER BY month
        ''')
        monthly_data = cursor.fetchall()
        stats['monthly_sentiment'] = {month: avg for month, avg in monthly_data}
        
        return stats
    
    def clear_database(self):
        """
        Clear all data from the database (useful for testing or resetting).
        
        Warning: This will delete all journal entries!
        """
        if self.conn is None:
            self._create_tables()
        
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM journal_entries')
        self.conn.commit()
        print("Database cleared")
    
    def close(self):
        """
        Close the database connection.
        
        Always call this when you're done with the database to free up resources.
        """
        if self.conn:
            self.conn.close()
            self.conn = None 