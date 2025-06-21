# 🧠 Mood Tracker & Journal Dashboard

A personal data project to visualize mood trends, sentiment, and themes from journal entries using Python, SQL, and Streamlit.

This lightweight dashboard ingests exported Notion journals and gives you insights like:
- Mood over time (using sentiment analysis)
- Word clouds of recurring topics
- Most common moods by weekday
- Entry filtering by time or keywords

**🔒 Privacy First:** Your journal data stays on your device and is never sent to external servers.

---

## 🔧 Tech Stack

- **Python 3.9+**
- **TextBlob** – for rule-based sentiment analysis
- **Streamlit** – interactive dashboard
- **SQLite** – local storage of processed entries
- **Pandas** – data wrangling
- **Matplotlib / WordCloud** – basic visualizations

---

## 📁 Project Structure

mood_tracker_dashboard/
├── data/
│   └── sample_journal_entries.csv    # Sample data (safe for GitHub)
├── app/
│   ├── dashboard.py                  # Streamlit app with file upload
│   ├── nlp_utils.py                  # TextBlob mood parsing
│   └── db.py                         # SQLite handling
├── notebooks/
│   └── mood_exploration.ipynb        # Prototyping + EDA
├── requirements.txt
├── .gitignore                        # Protects your personal data
└── README.md

---

## 🔒 Data Privacy

**Your personal journal data is protected:**

- ✅ **Local processing** - All analysis happens on your device
- ✅ **No external servers** - Data never leaves your computer
- ✅ **Secure upload** - Use the dashboard's file uploader
- ✅ **GitHub safe** - Personal data files are in `.gitignore`
- ✅ **Sample data only** - Repository contains only fictional examples

**Never commit your actual journal entries to version control!**

---

## 📤 Step 1: Prepare Your Data

### Option A: Use Sample Data (Recommended for testing)

The project includes sample journal entries in `data/sample_journal_entries.csv` that you can use to test the dashboard immediately.

### Option B: Convert Your Markdown Journal Files

If your Notion journal exports as Markdown files (like in `data/journal_1/`):

```bash
# Convert your Markdown files to CSV
python convert_journal.py

# Or use the all-in-one setup script
python setup_and_run.py
```

This will:
- Read all `.md` files from `data/journal_1/`
- Extract dates, titles, and content
- Convert to CSV format for the dashboard
- Launch the dashboard automatically

### Option C: Upload Your Personal Journal Data

1. **Export from Notion:**
   - Go to your Notion journal page
   - Click the "..." menu → "Export"
   - Choose "CSV" format
   - Download the file

2. **Upload in Dashboard:**
   - Launch the dashboard
   - Use the file uploader in the sidebar
   - Select your exported CSV file
   - Your data will be processed locally

**Expected CSV format:**
| date       | title           | content                     |
|------------|------------------|------------------------------|
| 2023-02-15 | Feeling Grateful | I had a hard day but I'm ok. |

---

## 📦 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Step 3: Run Sentiment Analysis

The dashboard automatically processes your journal entries using TextBlob for sentiment analysis:

```python
from textblob import TextBlob

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity
```

Results are stored locally in SQLite for privacy.

---

## 📊 Step 4: Launch the Dashboard

### Quick Launch (Recommended)
```bash
python run_dashboard.py
```

### Manual Launch
```bash
streamlit run app/dashboard.py
```

### Test Your Setup
```bash
python test_setup.py
```

The dashboard will open in your web browser at `http://localhost:8501`

---

## 🔧 Using the Dashboard

### Data Upload
1. **Upload your CSV** using the sidebar file uploader
2. **Verify format** - ensure columns: date, title, content
3. **Process automatically** - sentiment analysis runs locally

### Features
- **📊 Summary Statistics** - Overview of your mood patterns
- **📈 Mood Timeline** - See how your mood changes over time
- **📊 Mood Distribution** - Histogram of sentiment scores
- **🥧 Mood Categories** - Pie chart of mood types
- **📅 Weekly Patterns** - Average mood by day of week
- **☁️ Word Cloud** - Most common words in your entries

### Filtering Options
- **Date Range** - Filter entries by specific dates
- **Mood Filter** - Show only certain mood categories
- **Search** - Find entries containing specific words

---

## 🧪 Optional: Explore in Jupyter

You can use `notebooks/mood_exploration.ipynb` to:
- Experiment with mood scoring thresholds
- Group by week/month
- Test improvements to keyword extraction
- Create custom visualizations

---

## 🚀 Ideas for Later
- Add tagging or themes (gratitude, anxiety, energy)
- Use Hugging Face for deeper NLP
- Add journal entry editor into Streamlit
- Export weekly mood report as PDF or email
- Set up automated Notion exports

---

## 🔒 Privacy & Security

### What's Protected
- ✅ Your personal journal entries
- ✅ Sentiment analysis results
- ✅ Database files with your data
- ✅ Any uploaded CSV files

### What's Safe to Share
- ✅ Sample data files (fictional entries)
- ✅ Code and documentation
- ✅ Configuration files
- ✅ Test scripts

### Best Practices
- **Never commit** `data/journal_entries.csv` (your real data)
- **Use the uploader** instead of placing files in the data folder
- **Keep backups** of your personal data separately
- **Review .gitignore** before committing changes

---

## 📚 Credits
- **TextBlob** – Simple NLP library
- **Streamlit** – Beautiful dashboards with minimal code
- **WordCloud** – Visualize recurring words

---

🧘‍♂️ Built for reflection, clarity, and creative coding vibes.

**Remember:** This tool is designed to help you understand your patterns and improve your well-being. Your privacy and data security are our top priorities. 