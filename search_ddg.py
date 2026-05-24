#!/usr/bin/env python3
"""
Use DuckDuckGo image search to find free stock photos on Unsplash/Pexels.
"""
import json
import os
import subprocess
import urllib.parse
import time

OUTPUT_DIR = "/home/alexagent/projects/gas-inpex-site/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ddg_search_images(query, max_results=8):
    """Search DuckDuckGo for images without API key."""
    encoded = urllib.parse.quote(query)
    # DDG image search
    url = f"https://duckduckgo.com/i.js?q={encoded}&p=1&s=0&o=json&vqd=4"
    
    result = subprocess.run(
        ["curl", "-s", "-L", url, 
         "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
         "-H", "Accept: application/json, text/plain, */*",
         "-H", "Referer: https://duckduckgo.com/"],
        capture_output=True, text=True, timeout=15
    )
    
    try:
        data = json.loads(result.stdout)
        results = data.get("results", [])
        images = []
        for r in results[:max_results]:
            image_url = r.get("image", "")
            thumbnail = r.get("thumbnail", "")
            title = r.get("title", "")
            source = r.get("source", "")
            url = r.get("url", "")
            
            # Filter to only Unsplash and Pexels (free to use)
            if any(s in image_url for s in ["images.unsplash.com", "images.pexels.com", "cdn.pixabay.com"]):
                images.append({
                    "image_url": image_url,
                    "title": title,
                    "source": source,
                    "url": url,
                    "thumbnail": thumbnail,
                })
        
        return images
    except Exception as e:
        print(f"  DDG search error: {e}")
        print(f"  Response: {result.stdout[:300]}")
        return []

def main():
    queries = {
        "obj-boiler-house.jpg": "industrial boiler room",
        "obj-automation.jpg": "factory automation control room",
        "obj-cottage.jpg": "modern luxury house exterior",
        "obj-pipeline.jpg": "gas pipeline construction",
    }
    
    results = {}
    
    for filename, query in queries.items():
        print(f"\n{'='*60}")
        print(f"SEARCHING: {filename}")
        print(f"Query: {query}")
        
        images = ddg_search_images(query)
        print(f"  Found {len(images)} results on Unsplash/Pexels/Pixabay")
        
        if images:
            for i, img in enumerate(images):
                print(f"  {i+1}. {img['image_url'][:80]}...")
                print(f"     Title: {img['title']}")
        
        results[filename] = images
        time.sleep(1)  # Be polite to DDG
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for filename, images in results.items():
        if images:
            print(f"  {filename}: {len(images)} candidates")
        else:
            print(f"  {filename}: No candidates found")

if __name__ == "__main__":
    main()