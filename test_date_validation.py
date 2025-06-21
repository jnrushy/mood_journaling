#!/usr/bin/env python3
"""
Test script to validate dates in journal files.
This helps catch problematic dates before they cause conversion errors.
"""

import os
import re
from pathlib import Path
from datetime import datetime

def extract_date_from_filename(filename):
    """
    Extract date from filename using various patterns.
    Returns date string or None if no valid date found.
    """
    # Remove file extension and the long hash at the end
    name = re.sub(r'\s[a-f0-9]{32}$', '', os.path.splitext(filename)[0]).strip()
    
    # Pattern 1: Starts with DayOfWeek, e.g., "Friday 1 10 25"
    # Catches "Friday 1 10 25", "Monday 3 31 25"
    match = re.match(r'^(?:\w+)\s+(\d{1,2})\s+(\d{1,2})\s+(\d{2,4})', name)
    if match:
        month, day, year = match.groups()
        if len(year) == 2: year = '20' + year
        return f"{year}-{int(month):02d}-{int(day):02d}"

    # Pattern 2: Starts with numbers, e.g., "2 27 2022 Job Grateful List"
    match = re.match(r'^(\d{1,2})\s+(\d{1,2})\s+(\d{2,4})', name)
    if match:
        month, day, year = match.groups()
        if len(year) == 2: year = '20' + year
        return f"{year}-{int(month):02d}-{int(day):02d}"

    # Pattern 3: With month name, e.g., "Colonoscopy Friday August 5th 2022"
    month_map = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
    month_pattern = '|'.join(month_map.keys())
    # This regex is more flexible and looks for the pattern anywhere in the string
    match = re.search(fr'(?P<month_name>{month_pattern})[a-z]*\s+(?P<day>\d{{1,2}})(?:st|nd|rd|th)?(?:,)?\s+(?P<year>\d{{4}})', name, re.IGNORECASE)
    if match:
        parts = match.groupdict()
        month = month_map[parts['month_name'][:3].lower()]
        day = parts['day']
        year = parts['year']
        return f"{year}-{int(month):02d}-{int(day):02d}"

    return None

def is_valid_date(date_str):
    """
    Check if a date string represents a valid, reasonable date.
    """
    try:
        # Parse the date
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Check if year is reasonable (between 1900 and 2100)
        if date_obj.year < 1900 or date_obj.year > 2100:
            return False, f"Year {date_obj.year} is outside reasonable range (1900-2100)"
        
        # Check if date is in the future (more than 10 years from now)
        current_year = datetime.now().year
        if date_obj.year > current_year + 10:
            return False, f"Date {date_str} is more than 10 years in the future"
        
        # Check if date is too far in the past (more than 50 years ago)
        if date_obj.year < current_year - 50:
            return False, f"Date {date_str} is more than 50 years in the past"
        
        return True, "Valid date"
        
    except ValueError as e:
        return False, f"Invalid date format: {str(e)}"

def test_journal_dates():
    """
    Test all journal files for date validation issues.
    """
    journal_dir = Path("data/journal_1")
    
    if not journal_dir.exists():
        print("❌ Journal directory not found")
        return False
    
    # Get all markdown files
    md_files = list(journal_dir.glob("*.md"))
    
    if not md_files:
        print("❌ No markdown files found")
        return False
    
    print(f"🔍 Testing {len(md_files)} journal files for date validation...")
    print("=" * 60)
    
    issues_found = []
    valid_files = 0
    
    for md_file in md_files:
        # Extract date from filename
        date_str = extract_date_from_filename(md_file.name)
        
        if not date_str:
            issues_found.append({
                'file': md_file.name,
                'issue': 'No date found in filename',
                'severity': 'warning'
            })
            continue
        
        # Validate the date
        is_valid, message = is_valid_date(date_str)
        
        if is_valid:
            valid_files += 1
        else:
            issues_found.append({
                'file': md_file.name,
                'date': date_str,
                'issue': message,
                'severity': 'error'
            })
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results:")
    print(f"   ✅ Valid files: {valid_files}")
    print(f"   ❌ Issues found: {len(issues_found)}")
    
    if issues_found:
        print(f"\n🚨 Issues that need attention:")
        for issue in issues_found:
            severity_icon = "❌" if issue['severity'] == 'error' else "⚠️"
            print(f"   {severity_icon} {issue['file']}: {issue['issue']}")
        
        print(f"\n💡 Recommendations:")
        print(f"   - For files with 'No date found', consider renaming them to a standard format like 'YYYY-MM-DD Title.md' or 'Month Day Year Title.md'")
        print(f"   - Fix filenames with invalid dates (e.g., check for typos in years)")
        
        return False
    else:
        print(f"\n🎉 All files passed date validation!")
        return True

def main():
    """
    Main function to run date validation tests.
    """
    print("🧪 Journal Date Validation Test")
    print("=" * 40)
    
    success = test_journal_dates()
    
    if success:
        print("\n✅ All tests passed! Your journal files are ready for conversion.")
    else:
        print("\n❌ Some issues found. Please review the recommendations above and fix the files before running the conversion script.")
    
    return success

if __name__ == "__main__":
    main() 