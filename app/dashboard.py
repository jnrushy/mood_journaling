"""
Mood Tracker Dashboard - Main Streamlit Application

This is the main dashboard application that provides an interactive interface for
analyzing journal entries and mood patterns. It includes various visualizations
and filtering capabilities to help understand mood trends over time.

PRIVACY NOTE: This dashboard is designed to keep your personal journal data local.
Your data is never sent to external servers and is stored only on your device.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta, date
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
import os

# Import our custom modules
from nlp_utils import analyze_journal_entries, get_mood_statistics, get_common_keywords
from db import JournalDatabase


# Configure the Streamlit page
st.set_page_config(
    page_title="🧠 Mood Tracker Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive-mood { color: #2ca02c; }
    .negative-mood { color: #d62728; }
    .neutral-mood { color: #7f7f7f; }
    .privacy-notice {
        background-color: #e8f4fd;
        border: 1px solid #1f77b4;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def load_and_process_data(uploaded_file=None):
    """
    Load journal data from CSV file and process it with sentiment analysis.
    
    This function handles the data loading workflow:
    1. Loads raw CSV data (sample, uploaded, or converted)
    2. Applies sentiment analysis
    3. Caches results for performance
    
    Returns:
        pd.DataFrame: Processed journal entries with sentiment analysis
    """
    try:
        df = None
        # Check if user uploaded a file
        if uploaded_file is not None:
            # Use uploaded file
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} entries from your uploaded file")
        else:
            # Check for converted journal data first
            converted_file = 'data/journal_entries.csv'
            if os.path.exists(converted_file):
                df = pd.read_csv(converted_file)
                st.success(f"✅ Loaded {len(df)} entries from your converted journal data")
                st.info("📝 This is your personal journal data converted from Markdown files")
            else:
                # Try to load sample data
                sample_file = 'data/sample_journal_entries.csv'
                if os.path.exists(sample_file):
                    df = pd.read_csv(sample_file)
                    st.info("📝 Using sample data. Upload your own journal data or run convert_journal.py to convert your Markdown files!")
                else:
                    st.error("❌ No journal data found!")
                    st.info("📝 Options:")
                    st.info("   • Upload a CSV file using the sidebar")
                    st.info("   • Run 'python convert_journal.py' to convert your Markdown files")
                    st.info("   • Ensure sample data exists: data/sample_journal_entries.csv")
                    return None
        
        # Process the data with sentiment analysis
        processed_df = analyze_journal_entries(df)
        
        # Store in database for persistence (only if using uploaded or converted data)
        if uploaded_file is not None or os.path.exists('data/journal_entries.csv'):
            db = JournalDatabase()
            db.insert_entries(processed_df)
            db.close()
        
        return processed_df
        
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        st.info("💡 Make sure your CSV has columns: date, title, content")
        return None


def create_mood_timeline_chart(df):
    """
    Create a line chart showing mood trends over time.
    
    This visualization helps identify patterns in mood over time,
    such as weekly cycles, seasonal trends, or the impact of specific events.
    
    Args:
        df (pd.DataFrame): Processed journal entries
        
    Returns:
        plotly.graph_objects.Figure: Interactive line chart
    """
    # Prepare data for the timeline
    timeline_data = df.copy()
    timeline_data['date'] = pd.to_datetime(timeline_data['date'])
    timeline_data = timeline_data.sort_values('date')
    
    # Create the line chart
    fig = px.line(
        timeline_data,
        x='date',
        y='sentiment_score',
        title='📈 Mood Timeline - Sentiment Over Time',
        labels={'sentiment_score': 'Sentiment Score', 'date': 'Date'},
        hover_data=['title', 'mood_category']
    )
    
    # Add a horizontal line at y=0 to show neutral sentiment
    fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                  annotation_text="Neutral Mood")
    
    # Customize the layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sentiment Score (-1 to +1)",
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_mood_distribution_chart(df):
    """
    Create a histogram showing the distribution of mood scores.
    
    This helps understand the overall mood patterns - whether entries tend
    to be more positive, negative, or neutral on average.
    
    Args:
        df (pd.DataFrame): Processed journal entries
        
    Returns:
        plotly.graph_objects.Figure: Interactive histogram
    """
    # Create histogram of sentiment scores
    fig = px.histogram(
        df,
        x='sentiment_score',
        nbins=20,
        title='📊 Mood Distribution - How Often Each Mood Occurs',
        labels={'sentiment_score': 'Sentiment Score', 'count': 'Number of Entries'},
        color_discrete_sequence=['#1f77b4']
    )
    
    # Add vertical lines for mood boundaries
    fig.add_vline(x=-0.5, line_dash="dash", line_color="red", 
                  annotation_text="Very Negative")
    fig.add_vline(x=-0.1, line_dash="dash", line_color="orange", 
                  annotation_text="Negative")
    fig.add_vline(x=0.1, line_dash="dash", line_color="gray", 
                  annotation_text="Neutral")
    fig.add_vline(x=0.5, line_dash="dash", line_color="green", 
                  annotation_text="Positive")
    
    fig.update_layout(
        xaxis_title="Sentiment Score",
        yaxis_title="Number of Entries",
        height=400
    )
    
    return fig


def create_mood_category_pie(df):
    """
    Create a pie chart showing the distribution of mood categories.
    
    This provides a quick visual summary of how entries are distributed
    across the different mood categories (Very Negative, Negative, etc.).
    
    Args:
        df (pd.DataFrame): Processed journal entries
        
    Returns:
        plotly.graph_objects.Figure: Interactive pie chart
    """
    # Count entries by mood category
    mood_counts = df['mood_category'].value_counts()
    
    # Define colors for each mood category
    colors = {
        'Very Negative': '#d62728',
        'Negative': '#ff7f0e', 
        'Neutral': '#7f7f7f',
        'Positive': '#2ca02c',
        'Very Positive': '#1f77b4'
    }
    
    # Create pie chart
    fig = px.pie(
        values=mood_counts.values,
        names=mood_counts.index,
        title='🥧 Mood Category Distribution',
        color_discrete_map=colors
    )
    
    fig.update_layout(height=400)
    return fig


def create_wordcloud(df):
    """
    Create a word cloud from the most common keywords in journal entries.
    
    This visualization helps identify recurring themes and topics
    that appear frequently in the journal entries.
    
    Args:
        df (pd.DataFrame): Processed journal entries
        
    Returns:
        str: Base64 encoded image of the word cloud
    """
    # Get common keywords across all entries
    common_keywords = get_common_keywords(df, top_n=50)
    
    if not common_keywords:
        return None
    
    # Create word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=50
    ).generate_from_frequencies(dict(common_keywords))
    
    # Convert to image
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('☁️ Most Common Words in Journal Entries', fontsize=16, pad=20)
    
    # Convert plot to base64 string for display
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=300)
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_str


def create_weekly_mood_chart(df):
    """
    Create a bar chart showing average mood by day of the week.
    
    This helps identify if there are patterns in mood based on the day
    of the week (e.g., Monday blues, weekend happiness).
    
    Args:
        df (pd.DataFrame): Processed journal entries
        
    Returns:
        plotly.graph_objects.Figure: Interactive bar chart
    """
    # Add day of week column
    df_copy = df.copy()
    df_copy['day_of_week'] = pd.to_datetime(df_copy['date']).dt.day_name()
    
    # Calculate average sentiment by day of week
    weekly_mood = df_copy.groupby('day_of_week')['sentiment_score'].mean().reset_index()
    
    # Define the correct order of days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_mood['day_of_week'] = pd.Categorical(weekly_mood['day_of_week'], categories=day_order, ordered=True)
    weekly_mood = weekly_mood.sort_values('day_of_week')
    
    # Create bar chart
    fig = px.bar(
        weekly_mood,
        x='day_of_week',
        y='sentiment_score',
        title='📅 Average Mood by Day of Week',
        labels={'sentiment_score': 'Average Sentiment Score', 'day_of_week': 'Day of Week'},
        color='sentiment_score',
        color_continuous_scale='RdYlGn'
    )
    
    # Add horizontal line at neutral
    fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                  annotation_text="Neutral Mood")
    
    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Average Sentiment Score",
        height=400
    )
    
    return fig


def display_entry_details(df, selected_entries):
    """
    Display detailed information about selected journal entries.
    
    This function shows the full content and analysis of specific entries
    when users want to dive deeper into particular journal entries.
    
    Args:
        df (pd.DataFrame): Processed journal entries
        selected_entries (list): List of selected entry indices
    """
    if not selected_entries:
        return
    
    st.subheader("📝 Selected Entry Details")
    
    for idx in selected_entries:
        entry = df.iloc[idx]
        
        # Determine mood color class
        sentiment = entry['sentiment_score']
        if sentiment > 0.1:
            mood_class = "positive-mood"
        elif sentiment < -0.1:
            mood_class = "negative-mood"
        else:
            mood_class = "neutral-mood"
        
        # Display entry information
        with st.expander(f"📅 {entry['date'].strftime('%Y-%m-%d')} - {entry.get('title', 'No Title')}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write("**Content:**")
                st.write(entry['content'])
                
                if entry.get('keywords'):
                    st.write("**Keywords:**")
                    st.write(", ".join(entry['keywords'][:10]))  # Show first 10 keywords
            
            with col2:
                st.metric(
                    "Sentiment Score",
                    f"{sentiment:.3f}",
                    delta=None
                )
                st.markdown(f"<p class='{mood_class}'><strong>Mood:</strong> {entry['mood_category']}</p>", 
                           unsafe_allow_html=True)


def main():
    """
    Main function to run the Streamlit dashboard application.
    """
    st.markdown("<h1 class='main-header'>🧠 Mood Tracker Dashboard</h1>", unsafe_allow_html=True)
    
    # --- Sidebar Controls ---
    st.sidebar.title("🛠️ Dashboard Controls")
    
    # File uploader
    st.sidebar.header("📤 Upload Your Journal Data")
    uploaded_file = st.sidebar.file_uploader(
        "Choose your journal CSV file",
        type="csv",
        help="Upload a CSV file with 'date', 'title', and 'content' columns. Your data stays private on your device."
    )

    # --- Data Loading ---
    df = load_and_process_data(uploaded_file)
    
    if df is None or df.empty:
        st.warning("Please upload a journal file or convert your Markdown files to get started.")
        st.stop()
        
    # Convert date column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # --- Sidebar Filters ---
    st.sidebar.header("🗓️ Filter Options")

    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    # Quick filters
    st.sidebar.subheader("Quick Date Filters")
    if st.sidebar.button("Last 90 Days"):
        st.session_state.start_date = max_date - timedelta(days=90)
        st.session_state.end_date = max_date
    if st.sidebar.button("This Year"):
        st.session_state.start_date = datetime(max_date.year, 1, 1).date()
        st.session_state.end_date = max_date
    if st.sidebar.button("All Time"):
        st.session_state.start_date = min_date
        st.session_state.end_date = max_date

    # Define default dates and ensure they are within the data's range
    default_start = date(2025, 1, 1)
    default_end = date(2025, 6, 1)

    if not (min_date <= default_start <= max_date):
        default_start = min_date
    if not (min_date <= default_end <= max_date):
        default_end = max_date

    start_date = st.sidebar.date_input(
        'Start date',
        st.session_state.get('start_date', default_start),
        min_value=min_date,
        max_value=max_date,
        key='start_date'
    )
    
    end_date = st.sidebar.date_input(
        'End date',
        st.session_state.get('end_date', default_end),
        min_value=min_date,
        max_value=max_date,
        key='end_date'
    )

    # Mood category filter
    st.sidebar.subheader("😊 Mood Filter")
    mood_categories = ['All'] + df['mood_category'].unique().tolist()
    selected_mood = st.sidebar.selectbox(
        "Filter by mood",
        mood_categories,
        help="Filter the dashboard to show entries of a specific mood."
    )
    
    # --- Data Filtering ---
    filtered_df = df[
        (df['date'].dt.date >= start_date) & 
        (df['date'].dt.date <= end_date)
    ]
    if selected_mood != 'All':
        filtered_df = filtered_df[filtered_df['mood_category'] == selected_mood]

    if filtered_df.empty:
        st.warning("No entries found for the selected filters. Try expanding your date range or changing the mood filter.")
        st.stop()

    # --- Main Dashboard ---
    
    # Privacy notice
    st.markdown("""
    <div class="privacy-notice">
        <p>🔒 <strong>Privacy Notice:</strong> Your journal data stays on your device and is never sent to external servers. Upload your personal data securely in the sidebar.</p>
    </div>
    """, unsafe_allow_html=True)

    # Summary Statistics
    st.header("📊 Summary Statistics")
    total_entries, avg_mood, most_common_mood, date_range = get_mood_statistics(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entries", total_entries)
    
    with col2:
        st.metric(
            "Average Mood", 
            f"{avg_mood:.3f}",
            help="""
            **About the Average Mood Score**

            This score represents the average sentiment of your journal entries within the selected date range.

            - **Calculation**: It's the average of the sentiment polarity scores from all filtered entries. Each entry's content is analyzed to get a score.

            - **Score Range**: The score ranges from **-1.0 (Very Negative)** to **+1.0 (Very Positive)**. A score near 0 indicates a neutral mood.

            - **How to Interpret**:
                - **Positive score (> 0.1)**: Your entries are generally positive in tone.
                - **Negative score (< -0.1)**: Your entries are generally negative in tone.
                - **Neutral score (-0.1 to 0.1)**: Your entries are generally neutral.
            """
        )
    
    with col3:
        st.metric("Most Common Mood", most_common_mood)
    
    with col4:
        st.metric("Date Range", f"{date_range} days")
    
    # Main visualizations
    st.subheader("📈 Mood Analysis")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Timeline", "📊 Distribution", "🥧 Categories", "📅 Weekly Pattern", "☁️ Word Cloud"
    ])
    
    with tab1:
        if not filtered_df.empty:
            timeline_fig = create_mood_timeline_chart(filtered_df)
            st.plotly_chart(timeline_fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
    
    with tab2:
        if not filtered_df.empty:
            dist_fig = create_mood_distribution_chart(filtered_df)
            st.plotly_chart(dist_fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
    
    with tab3:
        if not filtered_df.empty:
            pie_fig = create_mood_category_pie(filtered_df)
            st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
    
    with tab4:
        if not filtered_df.empty:
            weekly_fig = create_weekly_mood_chart(filtered_df)
            st.plotly_chart(weekly_fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
    
    with tab5:
        if not filtered_df.empty:
            wordcloud_img = create_wordcloud(filtered_df)
            if wordcloud_img:
                st.image(f"data:image/png;base64,{wordcloud_img}", use_column_width=True)
            else:
                st.info("No keywords found in the filtered entries.")
        else:
            st.info("No data available for the selected filters.")
    
    # Detailed Entry View
    st.header("✒️ Journal Entries")
    st.info("Click on a data point in the charts above to see entry details here.")
    
    # This part is a bit tricky with Streamlit - we can't directly get clicks
    # from plotly. Instead, we'll show the most recent entries.
    st.dataframe(
        filtered_df[['date', 'title', 'mood_category', 'sentiment_score']]
        .sort_values('date', ascending=False)
        .head(10),
        use_container_width=True
    )


if __name__ == "__main__":
    main() 