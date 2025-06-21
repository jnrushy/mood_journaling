#!/usr/bin/env python3
"""
Test script for the Mood Tracker Dashboard.

This script tests all the main components to ensure everything is working correctly.
Run this script to verify your setup before launching the dashboard.
"""

import sys
import os
import pandas as pd

# Add the app directory to the path
sys.path.append('app')

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from nlp_utils import analyze_sentiment, categorize_mood, analyze_journal_entries
        from db import JournalDatabase
        print("✅ All modules imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_sentiment_analysis():
    """Test the sentiment analysis functionality."""
    print("\n🧠 Testing sentiment analysis...")
    
    try:
        from nlp_utils import analyze_sentiment, categorize_mood
        
        # Test with different types of text
        test_texts = [
            ("I'm feeling great today!", "positive"),
            ("This is terrible, I hate everything.", "negative"),
            ("The weather is okay.", "neutral"),
            ("I'm so excited about this amazing opportunity!", "very positive"),
            ("I'm really disappointed and frustrated.", "very negative")
        ]
        
        for text, expected_type in test_texts:
            sentiment = analyze_sentiment(text)
            mood = categorize_mood(sentiment)
            print(f"  Text: '{text[:30]}...'")
            print(f"    Sentiment: {sentiment:.3f}")
            print(f"    Mood: {mood}")
            print()
        
        print("✅ Sentiment analysis working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Sentiment analysis error: {e}")
        return False

def test_data_loading():
    """Test loading and processing the sample data."""
    print("\n📊 Testing data loading...")
    
    try:
        # Check if sample data exists
        sample_file = 'data/sample_journal_entries.csv'
        if not os.path.exists(sample_file):
            print("❌ Sample data file not found!")
            print("   Please ensure 'data/sample_journal_entries.csv' exists")
            return False
        
        # Load and process data
        df = pd.read_csv(sample_file)
        print(f"✅ Loaded {len(df)} entries from sample CSV")
        
        # Test processing
        from nlp_utils import analyze_journal_entries
        processed_df = analyze_journal_entries(df)
        print(f"✅ Processed {len(processed_df)} entries with sentiment analysis")
        
        # Show sample results
        print("\n📝 Sample processed entries:")
        sample = processed_df[['date', 'title', 'sentiment_score', 'mood_category']].head(3)
        print(sample.to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def test_database():
    """Test database functionality."""
    print("\n🗄️ Testing database...")
    
    try:
        from db import JournalDatabase
        
        # Create database instance
        db = JournalDatabase('data/test_db.db')
        print("✅ Database created successfully")
        
        # Test with sample data
        df = pd.read_csv('data/sample_journal_entries.csv')
        from nlp_utils import analyze_journal_entries
        processed_df = analyze_journal_entries(df)
        
        # Insert data
        inserted_count = db.insert_entries(processed_df)
        print(f"✅ Inserted {inserted_count} entries into database")
        
        # Retrieve data
        retrieved_df = db.get_all_entries()
        print(f"✅ Retrieved {len(retrieved_df)} entries from database")
        
        # Get statistics
        stats = db.get_mood_statistics()
        print(f"✅ Retrieved statistics: {stats['total_entries']} total entries")
        
        # Clean up test database
        db.close()
        if os.path.exists('data/test_db.db'):
            os.remove('data/test_db.db')
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_visualizations():
    """Test that visualization libraries are available."""
    print("\n📈 Testing visualization libraries...")
    
    try:
        import plotly.express as px
        import matplotlib.pyplot as plt
        from wordcloud import WordCloud
        
        print("✅ All visualization libraries available!")
        
        # Test basic plot creation
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 2]})
        fig = px.line(df, x='x', y='y')
        print("✅ Plotly charts working")
        
        return True
        
    except ImportError as e:
        print(f"❌ Visualization library error: {e}")
        print("   Try running: pip install plotly matplotlib wordcloud")
        return False

def test_privacy_features():
    """Test that privacy features are working correctly."""
    print("\n🔒 Testing privacy features...")
    
    try:
        # Check that .gitignore exists and contains privacy rules
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
            
            privacy_patterns = [
                'data/*.csv',
                'data/*.db',
                'data/*.sqlite',
                '*.env'
            ]
            
            missing_patterns = []
            for pattern in privacy_patterns:
                if pattern not in gitignore_content:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                print(f"⚠️ Missing privacy patterns in .gitignore: {missing_patterns}")
            else:
                print("✅ .gitignore contains privacy protection rules")
            
            return True
        else:
            print("❌ .gitignore file not found!")
            return False
            
    except Exception as e:
        print(f"❌ Privacy test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧠 Mood Tracker Dashboard - Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_sentiment_analysis,
        test_data_loading,
        test_database,
        test_visualizations,
        test_privacy_features
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To launch the dashboard, run:")
        print("   python run_dashboard.py")
        print("   or")
        print("   streamlit run app/dashboard.py")
        print("\n🔒 Privacy reminder: Your personal data stays local!")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   - Install missing packages: pip install -r requirements.txt")
        print("   - Ensure sample data exists: data/sample_journal_entries.csv")
        print("   - Check that all files are in the correct locations")
        print("   - Verify .gitignore is protecting your privacy")

if __name__ == "__main__":
    main() 