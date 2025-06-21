# 🚀 Setup Guide - Mood Tracker Dashboard

This guide will walk you through setting up and running your personal mood tracking dashboard.

## 📋 Prerequisites

- **Python 3.9 or higher** (check with `python --version`)
- **pip** (Python package installer)
- **Web browser** (Chrome, Firefox, Safari, etc.)

## 🔒 Privacy First

**Your personal journal data is protected:**
- ✅ **Local processing** - All analysis happens on your device
- ✅ **No external servers** - Data never leaves your computer
- ✅ **Secure upload** - Use the dashboard's file uploader
- ✅ **GitHub safe** - Personal data files are in `.gitignore`
- ✅ **Sample data only** - Repository contains only fictional examples

**Never commit your actual journal entries to version control!**

## 🛠️ Step 1: Install Dependencies

First, install all the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- **Streamlit** - For the web dashboard
- **TextBlob** - For sentiment analysis
- **Pandas** - For data processing
- **Plotly** - For interactive charts
- **Matplotlib** - For basic plotting
- **WordCloud** - For word cloud visualizations

## 📊 Step 2: Test Your Setup

Run the test script to verify everything is working:

```bash
python test_setup.py
```

This will check:
- ✅ All dependencies are installed
- ✅ Sentiment analysis is working
- ✅ Sample data loading and processing
- ✅ Database functionality
- ✅ Visualization libraries
- ✅ Privacy protection (`.gitignore`)

## 🚀 Step 3: Launch the Dashboard

### Quick Launch (Recommended)
```bash
python run_dashboard.py
```

### Manual Launch
```bash
streamlit run app/dashboard.py
```

The dashboard will open in your web browser at `http://localhost:8501`

## 📁 Step 4: Add Your Personal Data

### Option A: Use Sample Data (Recommended for testing)

The dashboard will automatically load sample data so you can test all features immediately.

### Option B: Upload Your Personal Journal Data

1. **Export from Notion:**
   - Go to your Notion journal page
   - Click the "..." menu → "Export"
   - Choose "CSV" format
   - Download the file

2. **Upload in Dashboard:**
   - Use the file uploader in the sidebar
   - Select your exported CSV file
   - Your data will be processed locally and securely

**Expected CSV format:**
```csv
date,title,content
2024-01-15,Feeling Grateful,"Today was amazing! I had a great conversation..."
2024-01-16,Productive Day,"Work was really productive today..."
```

## 📖 Using the Dashboard

### Data Upload & Privacy
- **🔒 Secure upload** - Files are processed locally only
- **📝 Sample data** - Start with fictional examples
- **🔄 Easy switching** - Upload your data anytime
- **🗄️ Local storage** - Data stored in SQLite on your device

### Main Features:
1. **📊 Summary Statistics** - Overview of your mood patterns
2. **📈 Mood Timeline** - See how your mood changes over time
3. **📊 Mood Distribution** - Histogram of sentiment scores
4. **🥧 Mood Categories** - Pie chart of mood types
5. **📅 Weekly Patterns** - Average mood by day of week
6. **☁️ Word Cloud** - Most common words in your entries

### Filtering Options:
- **Date Range** - Filter entries by specific dates
- **Mood Filter** - Show only certain mood categories
- **Search** - Find entries containing specific words

### Interactive Features:
- **Hover over charts** for detailed information
- **Click and drag** to zoom in on timeline
- **Browse entries** to read full journal content
- **Export data** for further analysis

## 🔧 Customization

### Adjusting Mood Thresholds

The sentiment analysis categorizes moods into 5 levels. You can adjust these thresholds in `app/nlp_utils.py`:

```python
def categorize_mood(sentiment_score: float) -> str:
    if sentiment_score <= -0.5:      # Very Negative threshold
        return "Very Negative"
    elif sentiment_score <= -0.1:    # Negative threshold
        return "Negative"
    elif sentiment_score <= 0.1:     # Neutral threshold
        return "Neutral"
    elif sentiment_score <= 0.5:     # Positive threshold
        return "Positive"
    else:
        return "Very Positive"
```

### Adding Custom Keywords

You can modify the keyword extraction in `app/nlp_utils.py` to focus on specific themes:

```python
def extract_keywords(text: str, min_length: int = 4, max_words: int = 50) -> List[str]:
    # Add your custom stop words or keywords here
    custom_stop_words = {'your', 'custom', 'words'}
    # ... rest of function
```

## 🧪 Advanced Usage

### Jupyter Notebook Exploration

For deeper analysis, use the Jupyter notebook:

```bash
cd notebooks
jupyter notebook mood_exploration.ipynb
```

This notebook lets you:
- Experiment with different analysis approaches
- Test custom mood thresholds
- Create custom visualizations
- Export insights

### Database Access

The dashboard stores processed data in SQLite. You can access it directly:

```python
from app.db import JournalDatabase

db = JournalDatabase()
entries = db.get_all_entries()
stats = db.get_mood_statistics()
```

## 🔒 Privacy & Security

### What's Protected by .gitignore
- ✅ Your personal journal entries (`data/*.csv`)
- ✅ Database files with your data (`data/*.db`, `data/*.sqlite`)
- ✅ Environment variables (`.env` files)
- ✅ Any uploaded CSV files

### What's Safe to Share
- ✅ Sample data files (fictional entries)
- ✅ Code and documentation
- ✅ Configuration files
- ✅ Test scripts

### Best Practices
- **Never commit** your actual journal data
- **Use the uploader** instead of placing files in the data folder
- **Keep backups** of your personal data separately
- **Review .gitignore** before committing changes

## 🐛 Troubleshooting

### Common Issues:

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**Dashboard won't start:**
```bash
python test_setup.py  # Check for issues
streamlit run app/dashboard.py --server.port 8502  # Try different port
```

**No data showing:**
- Check that `data/sample_journal_entries.csv` exists (for testing)
- Upload your personal data using the sidebar uploader
- Verify CSV format has `date`, `title`, `content` columns
- Ensure dates are in `YYYY-MM-DD` format

**Slow performance:**
- Reduce the number of entries in your CSV
- Close other applications using Python
- Try running on a different port

**Privacy concerns:**
- Verify `.gitignore` contains privacy rules
- Use the file uploader instead of placing files in data folder
- Check that no personal data is being committed

### Getting Help:

1. **Check the test script output** for specific errors
2. **Verify your CSV format** matches the example
3. **Check Python version** (needs 3.9+)
4. **Review the logs** in the terminal for error messages
5. **Ensure privacy protection** is working correctly

## 📈 Next Steps

Once you're comfortable with the basic dashboard:

1. **Upload your real journal data** using the sidebar uploader
2. **Experiment with the Jupyter notebook** for custom analysis
3. **Customize the mood thresholds** to better match your writing style
4. **Add new visualizations** based on your interests
5. **Set up regular data updates** from your Notion journal

## 🎯 Tips for Best Results

- **Write consistently** - Regular entries provide better patterns
- **Be honest** - The analysis works best with authentic content
- **Include context** - More detailed entries give richer insights
- **Review regularly** - Check your dashboard weekly to spot trends
- **Export backups** - Keep copies of your data for safety
- **Respect privacy** - Never share your personal journal data

---

**Happy mood tracking! 🧠✨**

Remember: This tool is designed to help you understand your patterns and improve your well-being. Your privacy and data security are our top priorities. 