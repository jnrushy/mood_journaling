#!/usr/bin/env python3
"""
Journal Markdown to CSV Converter

This script converts your Notion journal Markdown files into CSV format
that can be processed by the Mood Tracker Dashboard.

The script:
1. Reads all .md files from the journal_1 directory
2. Extracts date, title, and content from each file
3. Converts to CSV format with columns: date, title, content
4. Handles various date formats and file naming patterns
"""

import os
import re
import pandas as pd
from datetime import datetime
from pathlib import Path
import argparse


def extract_date_from_filename(filename):
    """
    Extract date from filename using various patterns.
    Returns date string or None if no valid date found.
    """
    # Remove file extension and the long hash at the end
    name = re.sub(r'\s[a-f0-9]{32}$', '', os.path.splitext(filename)[0]).strip()
    
    # Try to extract title by removing the date part
    title = name

    # Pattern 1: Starts with DayOfWeek, e.g., "Friday 1 10 25"
    match = re.match(r'^(?:\w+)\s+(\d{1,2})\s+(\d{1,2})\s+(\d{2,4})', name)
    if match:
        month, day, year = match.groups()
        if len(year) == 2: year = '20' + year
        date_str = f"{year}-{int(month):02d}-{int(day):02d}"
        # Extract title by removing the matched part
        title = name[match.end():].strip().lstrip('-').strip()
        return date_str, title

    # Pattern 2: Starts with numbers, e.g., "2 27 2022"
    match = re.match(r'^(\d{1,2})\s+(\d{1,2})\s+(\d{2,4})', name)
    if match:
        month, day, year = match.groups()
        if len(year) == 2: year = '20' + year
        date_str = f"{year}-{int(month):02d}-{int(day):02d}"
        title = name[match.end():].strip().lstrip('-').strip()
        return date_str, title

    # Pattern 3: With month name, e.g., "August 5th 2022"
    month_map = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
    month_pattern = '|'.join(month_map.keys())
    match = re.search(fr'(?P<month_name>{month_pattern})[a-z]*\s+(?P<day>\d{{1,2}})(?:st|nd|rd|th)?(?:,)?\s+(?P<year>\d{{4}})', name, re.IGNORECASE)
    if match:
        parts = match.groupdict()
        month = month_map[parts['month_name'][:3].lower()]
        day = parts['day']
        year = parts['year']
        date_str = f"{year}-{int(month):02d}-{int(day):02d}"
        # A bit trickier to get title here, we'll just use the whole name for now
        return date_str, name

    return None, name # Return original name as title if no date found


def get_entry_details(md_file):
    """
    Extracts date, title, and content from a markdown file.
    """
    filename = md_file.name
    content = md_file.read_text(encoding='utf-8')

    # 1. Get date and title from filename
    date_str, title_from_filename = extract_date_from_filename(filename)

    # 2. Extract title from content if available
    lines = content.split('\n')
    title_from_content = None
    content_lines = []
    in_content = False

    for i, line in enumerate(lines):
        if line.startswith('# ') and title_from_content is None:
            title_from_content = line[2:].strip()
            # If the next line is blank, skip it
            if i + 1 < len(lines) and not lines[i+1].strip():
                continue
        elif line.startswith('Created:') or line.startswith('Updated:'):
            continue
        else:
            content_lines.append(line)

    final_title = title_from_content or title_from_filename or "Untitled Entry"
    final_content = '\n'.join(content_lines).strip()

    return date_str, final_title, final_content


def convert_journal_files(journal_dir='data/journal_1', output_file='data/journal_entries.csv'):
    """
    Convert all Markdown journal files to CSV format
    """
    journal_path = Path(journal_dir)
    
    if not journal_path.exists():
        print(f"❌ Journal directory not found: {journal_dir}")
        return None
    
    entries = []
    
    # Get all .md files
    md_files = list(journal_path.glob('*.md'))
    print(f"📁 Found {len(md_files)} journal entries")
    
    processed_files = 0
    skipped_files = 0
    
    for md_file in md_files:
        try:
            date_str, title, content = get_entry_details(md_file)
            
            if date_str:
                entries.append({
                    'date': date_str,
                    'title': title,
                    'content': content
                })
                processed_files += 1
            else:
                print(f"⚠️  Skipping '{md_file.name}': Could not determine a valid date.")
                skipped_files += 1

        except Exception as e:
            print(f"❌ Error processing '{md_file.name}': {e}")
            skipped_files += 1
            
    if not entries:
        print("❌ No entries were successfully processed.")
        return None
        
    # Create DataFrame and save to CSV
    df = pd.DataFrame(entries)
    
    # Validate and convert date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop entries that failed date conversion
    original_count = len(df)
    df.dropna(subset=['date'], inplace=True)
    if len(df) < original_count:
        print(f"⚠️  Dropped {original_count - len(df)} entries with invalid date formats after conversion.")
        
    df.sort_values(by='date', inplace=True)
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Successfully converted {processed_files} journal entries.")
    if skipped_files > 0:
        print(f"   (Skipped {skipped_files} files due to missing dates or errors)")
    print(f"   Saved to: {output_file}")
    
    return output_file


def main():
    """
    Main function to run the journal conversion script.
    """
    parser = argparse.ArgumentParser(description="Convert journal markdown files to CSV.")
    parser.add_argument(
        "--journal_dir",
        default="data/journal_1",
        help="Directory containing journal markdown files."
    )
    parser.add_argument(
        "--output_file",
        default="data/journal_entries.csv",
        help="Path to save the output CSV file."
    )
    args = parser.parse_args()
    
    print("🚀 Starting journal conversion...")
    convert_journal_files(args.journal_dir, args.output_file)
    print("✅ Conversion complete.")


if __name__ == "__main__":
    main() 