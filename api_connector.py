import requests
import configparser
import json
import csv
from datetime import datetime
from google_sheets import export_to_google_sheets

def clean_cell_content(text, max_length=40000):  # Reduced max length for safety
    """Ensure cell content doesn't exceed Google Sheets limit"""
    if not text:
        return ''
    cleaned = str(text).strip()
    if len(cleaned) > max_length:
        print(f"Warning: Content length {len(cleaned)} exceeds limit of {max_length} characters - will be skipped")
        return None
    return cleaned

def export_to_csv(data, filename=None):
    """Export listings data to CSV file"""
    if filename is None:
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'craigslist_listings_{timestamp}.csv'
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'price', 'location', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in data:
                # Only write the fields we want
                row = {
                    'title': item.get('title', ''),
                    'price': item.get('price', ''),
                    'location': item.get('location', ''),
                    'url': item.get('url', '')
                }
                writer.writerow(row)
        
        print(f"Successfully exported {len(data)} listings to {filename}")
        return True
    except Exception as e:
        print(f"Failed to export to CSV: {e}")
        return False

def get_craigslist_automotive_data():
    url = "https://craigslist-data.p.rapidapi.com/for-sale"
    
    payload = {
        "query": "cars",
        "gl": "newyork",
        "hl": "en",
        "has_pic": False,
        "posted_today": False,
        "show_duplicates": False,
        "search_title_only": False,
        "search_distance": 0,
        "page": 0,
        "purveyor": "",
        "min_price": 0,
        "max_price": 0,
        "auto_make_model": "",
        "crypto_currency_ok": False,
        "delivery_available": False
    }
    
    headers = {
        "x-rapidapi-key": "a615163a6bmsh934f80edac1a5e3p14bcd0jsn9044f4494977",
        "x-rapidapi-host": "craigslist-data.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        print("Fetching data from Craigslist API...")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        json_data = response.json()
        listings = json_data.get('data', [])
        
        if not listings:
            print("No listings found in the data")
            return
            
        # Export to CSV first
        export_to_csv(listings)
        
        print(f"Processing {len(listings)} listings for Google Sheets...")
        
        # Prepare data for Google Sheets with stricter limits
        headers = ['Title', 'Price', 'Location', 'URL']
        rows = [headers]  # Start with headers
        
        skipped_count = 0
        # Add each listing as a row with truncated content
        for item in listings:
            row = [
                clean_cell_content(item.get('title', '')),
                clean_cell_content(item.get('price', ''), max_length=100),  # Price shouldn't be long
                clean_cell_content(item.get('location', ''), max_length=200),  # Location shouldn't be long
                clean_cell_content(item.get('url', ''), max_length=1000)  # URLs shouldn't exceed 1000 chars
            ]
            
            # Skip row if any cell was too large (returned None)
            if None in row:
                skipped_count += 1
                continue
                
            rows.append(row)
        
        print(f"Prepared {len(rows)-1} valid rows for export (skipped {skipped_count} rows with oversized cells)")
        
        if len(rows) <= 1:
            print("No valid data to export after filtering")
            return
        
        # Export to Google Sheets
        spreadsheet_id = '1k7XRNbQUMWSXtSiljeBo1nuTYj8p7gBAHutCYqBzOEw'
        range_name = 'Sheet1!A1'
        
        print("Exporting to Google Sheets...")
        body = {"values": rows}
        
        success = export_to_google_sheets(body, spreadsheet_id, range_name)
        if success:
            print("Successfully exported to Google Sheets")
        else:
            print("Failed to export to Google Sheets")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Try loading existing JSON data first
    try:
        print("Attempting to load existing JSON data...")
        with open('craigslist_data.json', 'r') as f:
            json_data = json.load(f)
            listings = json_data.get('data', [])
            if listings:
                print(f"Found {len(listings)} listings in JSON file")
                # Export to CSV with custom filename
                csv_filename = f'craigslist_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                if export_to_csv(listings, csv_filename):
                    print(f"Successfully exported data to {csv_filename}")
            else:
                print("No listings found in JSON file")
    except FileNotFoundError:
        print("No existing JSON file found, fetching new data...")
        # If no JSON file exists, fetch new data
        get_craigslist_automotive_data()
    except Exception as e:
        print(f"Error processing data: {e}")