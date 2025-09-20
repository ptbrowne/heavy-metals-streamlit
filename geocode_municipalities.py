#!/usr/bin/env python3
"""
Script to geocode Swiss municipalities for the heavy metals monitoring data.
This script extracts unique municipalities from data.csv and geocodes them using
the OpenStreetMap Nominatim API, storing results in municipalities_geocoded.csv.
"""

import pandas as pd
import requests
import time
import csv
from typing import Tuple, Optional

def geocode_municipality(municipality: str, country: str = "Switzerland") -> Tuple[Optional[float], Optional[float]]:
    """
    Geocode a municipality using the Nominatim API.
    
    Args:
        municipality: The municipality name to geocode
        country: The country name (default: "Switzerland")
    
    Returns:
        Tuple of (latitude, longitude) or (None, None) if not found
    """
    # Nominatim API endpoint
    url = "https://nominatim.openstreetmap.org/search"
    
    # Parameters for the request
    params = {
        'q': f"{municipality}, {country}",
        'format': 'json',
        'limit': 1,
        'addressdetails': 1
    }
    
    # Add user agent as required by Nominatim
    headers = {
        'User-Agent': 'Heavy-Metals-Monitoring-App/1.0'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            print(f"✓ Found coordinates for {municipality}: ({lat:.4f}, {lon:.4f})")
            return lat, lon
        else:
            print(f"✗ No coordinates found for {municipality}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error geocoding {municipality}: {e}")
        return None, None
    except (KeyError, ValueError, IndexError) as e:
        print(f"✗ Error parsing response for {municipality}: {e}")
        return None, None

def extract_unique_municipalities(csv_file: str) -> list:
    """
    Extract unique municipalities from the data CSV file.
    
    Args:
        csv_file: Path to the data CSV file
    
    Returns:
        List of unique municipality names
    """
    df = pd.read_csv(csv_file)
    municipalities = df['Municipality'].unique().tolist()
    print(f"Found {len(municipalities)} unique municipalities")
    return sorted(municipalities)

def geocode_all_municipalities(municipalities: list, output_file: str):
    """
    Geocode all municipalities and save results to CSV.
    
    Args:
        municipalities: List of municipality names
        output_file: Path to output CSV file
    """
    results = []
    
    print(f"Starting geocoding of {len(municipalities)} municipalities...")
    print("This may take a few minutes due to API rate limiting.")
    
    for i, municipality in enumerate(municipalities, 1):
        print(f"[{i}/{len(municipalities)}] Geocoding {municipality}...")
        
        lat, lon = geocode_municipality(municipality)
        
        results.append({
            'Municipality': municipality,
            'Latitude': lat,
            'Longitude': lon
        })
        
        # Be respectful to the API - add a small delay
        time.sleep(1)
        
        # Save progress every 10 municipalities in case of interruption
        if i % 10 == 0:
            save_results(results, output_file)
            print(f"Progress saved after {i} municipalities")
    
    # Final save
    save_results(results, output_file)
    
    # Summary
    successful = sum(1 for r in results if r['Latitude'] is not None)
    failed = len(results) - successful
    
    print(f"\nGeocoding completed!")
    print(f"✓ Successfully geocoded: {successful} municipalities")
    print(f"✗ Failed to geocode: {failed} municipalities")
    print(f"Results saved to: {output_file}")

def save_results(results: list, output_file: str):
    """Save geocoding results to CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Municipality', 'Latitude', 'Longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def main():
    """Main function to run the geocoding process."""
    input_file = "data.csv"
    output_file = "municipalities_geocoded.csv"
    
    print("Heavy Metals Monitoring - Municipality Geocoding")
    print("=" * 50)
    
    # Check if input file exists
    try:
        municipalities = extract_unique_municipalities(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        return
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return
    
    # Start geocoding
    geocode_all_municipalities(municipalities, output_file)

if __name__ == "__main__":
    main()