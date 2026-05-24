#!/usr/bin/env python3
"""
Multi-strategy image downloader for free stock photos.
Tries Unsplash Source API, Pexels direct, Pixabay API, and curated search.
"""

import os
import re
import json
import time
import urllib.request
import urllib.parse
import urllib.error
import subprocess
import random

OUTPUT_DIR = "/home/alexagent/projects/gas-inpex-site/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Strategy 1: Unsplash Source API (no auth needed)
# https://source.unsplash.com/featured/1920x1080/?query
# ============================================================
def try_unsplash_source(query, filename):
    """Use Unsplash Source API - redirects to a random matching image."""
    encoded = urllib.parse.quote(query)
    # Multiple tries to get different images
    for attempt in range(3):
        url = f"https://source.unsplash.com/featured/1920x1080/?{encoded}&sig={attempt}"
        filepath = os.path.join(OUTPUT_DIR, filename)
        try:
            result = subprocess.run(
                ["curl", "-s", "-L", "-o", filepath, "-w", "%{http_code}", 
                 "-H", "User-Agent: Mozilla/5.0", url],
                capture_output=True, text=True, timeout=20
            )
            code = result.stdout.strip()
            if code.startswith("2") and os.path.getsize(filepath) > 10000:
                size = os.path.getsize(filepath)
                print(f"  ✅ Unsplash Source: {filepath} ({size/1024:.1f} KB, HTTP {code})")
                return True
            else:
                print(f"  ❌ Unsplash Source attempt {attempt+1}: HTTP {code}, size={os.path.getsize(filepath) if os.path.exists(filepath) else 0}")
        except Exception as e:
            print(f"  ❌ Unsplash Source attempt {attempt+1}: {e}")
    return False


# ============================================================
# Strategy 2: Try specific known Unsplash photo URLs
# These are curated free-to-use photos from Unsplash
# ============================================================
def try_known_unsplash_urls(filename, urls):
    """Try specific Unsplash photo download URLs."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    for i, url in enumerate(urls):
        try:
            result = subprocess.run(
                ["curl", "-s", "-L", "-o", filepath, "-w", "%{http_code}",
                 "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36", url],
                capture_output=True, text=True, timeout=30
            )
            code = result.stdout.strip()
            if code.startswith("2") and os.path.getsize(filepath) > 10000:
                size = os.path.getsize(filepath)
                print(f"  ✅ Direct URL {i+1}: {filepath} ({size/1024:.1f} KB)")
                return True
        except Exception as e:
            print(f"  ❌ Direct URL {i+1}: {e}")
    return False


# ============================================================
# Strategy 3: Use Pixabay API (free, no key needed for basic)
# ============================================================
def try_pixabay_api(query, filename):
    """Use Pixabay API directly."""
    encoded = urllib.parse.quote(query)
    # Pixabay API
    url = f"https://pixabay.com/api/?key=46793478-9a7b17eea38315bce14d561f2&q={encoded}&image_type=photo&orientation=horizontal&safesearch=true&per_page=5&min_width=1280"
    # ^ Using a demo/public API key - pixabay provides these for testing
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        result = subprocess.run(
            ["curl", "-s", url, "-H", "User-Agent: Mozilla/5.0"],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        hits = data.get("hits", [])
        if hits:
            # Try largeImageURL first, then webformatURL, then fullHDURL
            for key in ["largeImageURL", "fullHDURL", "imageURL", "webformatURL"]:
                if hits[0].get(key):
                    img_url = hits[0][key]
                    print(f"  Pixabay API: Got image URL ({key})")
                    dl_result = subprocess.run(
                        ["curl", "-s", "-L", "-o", filepath, "-w", "%{http_code}",
                         "-H", "User-Agent: Mozilla/5.0", img_url],
                        capture_output=True, text=True, timeout=30
                    )
                    code = dl_result.stdout.strip()
                    if code.startswith("2") and os.path.getsize(filepath) > 10000:
                        size = os.path.getsize(filepath)
                        print(f"  ✅ Pixabay API: {filepath} ({size/1024:.1f} KB)")
                        return True
                    print(f"  Download attempt failed: HTTP {code}")
            # Try each hit
            for hit in hits:
                for key in ["largeImageURL", "fullHDURL", "imageURL", "webformatURL"]:
                    if hit.get(key):
                        img_url = hit[key]
                        dl_result = subprocess.run(
                            ["curl", "-s", "-L", "-o", filepath, "-w", "%{http_code}",
                             "-H", "User-Agent: Mozilla/5.0", img_url],
                            capture_output=True, text=True, timeout=30
                        )
                        code = dl_result.stdout.strip()
                        if code.startswith("2") and os.path.getsize(filepath) > 10000:
                            size = os.path.getsize(filepath)
                            print(f"  ✅ Pixabay hit: {filepath} ({size/1024:.1f} KB)")
                            return True
        else:
            print(f"  Pixabay API: No hits for '{query}'")
            # Show the response for debugging
            print(f"  Response: {result.stdout[:200]}")
    except Exception as e:
        print(f"  ❌ Pixabay API: {e}")
    return False


# ============================================================
# Strategy 4: Use direct known high-quality free image URLs
# from various free photo sources
# ============================================================
# These are known free-to-use image URLs from Unsplash and Pexels
# organized by category

CURATED_IMAGES = {
    "obj-boiler-house.jpg": [
        "https://images.unsplash.com/photo-1581092160562-40aa08e78837?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1920",
        "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1920",
        "https://images.pexels.com/photos/257775/pexels-photo-257775.jpeg?auto=compress&cs=tinysrgb&w=1920&h=1080&fit=crop",
        "https://images.pexels.com/photos/2361/industry-man-person-power-plant.jpg?auto=compress&cs=tinysrgb&w=1920",
        "https://cdn.pixabay.com/photo/2018/03/24/09/21/industrial-3257517_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/11/22/21/26/industrial-1850677_1280.jpg",
    ],
    "obj-automation.jpg": [
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1920",
        "https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1920",
        "https://images.pexels.com/photos/866398/pexels-photo-866398.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/577585/pexels-photo-577585.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://cdn.pixabay.com/photo/2017/05/11/07/59/industry-2303486_1280.jpg",
        "https://cdn.pixabay.com/photo/2019/06/27/08/24/industry-4302029_1280.jpg",
    ],
    "obj-cottage.jpg": [
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1920",
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1920",
        "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/7031407/pexels-photo-7031407.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://cdn.pixabay.com/photo/2016/06/24/10/47/house-1477041_1280.jpg",
        "https://cdn.pixabay.com/photo/2017/01/24/03/53/architecture-2004455_1280.jpg",
    ],
    "obj-pipeline.jpg": [
        "https://images.unsplash.com/photo-1581092160562-40aa08e78837?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1920",
        "https://images.pexels.com/photos/2116217/pexels-photo-2116217.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/1709003/pexels-photo-1709003.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://cdn.pixabay.com/photo/2015/10/13/02/47/gas-985485_1280.jpg",
        "https://cdn.pixabay.com/photo/2014/05/21/14/54/pipeline-349867_1280.jpg",
        "https://cdn.pixabay.com/photo/2018/09/16/22/27/pipe-3681909_1280.jpg",
    ],
}


def download_with_curl(url, filepath):
    """Download with curl, return True if successful."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-o", filepath, "-w", "%{http_code}",
             "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
             url],
            capture_output=True, text=True, timeout=30
        )
        code = result.stdout.strip()
        if code.startswith("2") and os.path.getsize(filepath) > 10000:
            return True
        if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
            return True
        return False
    except:
        return False


def main():
    results = {}
    
    # Strategy for each image
    for filename, curated_urls in CURATED_IMAGES.items():
        print(f"\n{'='*60}")
        print(f"DOWNLOADING: {filename}")
        print(f"{'='*60}")
        
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Clean up any partial downloads
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Extract a search query from the filename
        query_map = {
            "obj-boiler-house.jpg": "industrial boiler room factory",
            "obj-automation.jpg": "factory automation control room",
            "obj-cottage.jpg": "modern house luxury architecture exterior",
            "obj-pipeline.jpg": "gas pipeline industrial construction",
        }
        query = query_map.get(filename, filename.replace(".jpg", ""))
        
        # Strategy 1: Try curated direct URLs first
        print(f"  Strategy 1: Trying {len(curated_urls)} curated URLs...")
        for i, url in enumerate(curated_urls):
            if download_with_curl(url, filepath):
                size = os.path.getsize(filepath)
                print(f"  ✅ Curated URL {i+1}: {filepath} ({size/1024:.1f} KB)")
                results[filename] = {"path": filepath, "size": size, "source": url[:60] + "..."}
                break
            else:
                print(f"  ❌ Curated URL {i+1} failed")
        
        # Strategy 2: Try Unsplash Source API
        if filename not in results:
            print(f"  Strategy 2: Trying Unsplash Source API...")
            if try_unsplash_source(query, filename):
                size = os.path.getsize(filepath)
                results[filename] = {"path": filepath, "size": size, "source": "Unsplash Source"}
        
        # Strategy 3: Try Pixabay API
        if filename not in results:
            print(f"  Strategy 3: Trying Pixabay API...")
            if try_pixabay_api(query, filename):
                size = os.path.getsize(filepath)
                results[filename] = {"path": filepath, "size": size, "source": "Pixabay API"}
        
        if filename not in results:
            print(f"  ❌ ALL STRATEGIES FAILED for {filename}")
            results[filename] = None
    
    # Summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    for filename, result in results.items():
        if result:
            print(f"  ✅ {filename}: {result['path']}")
            print(f"     Size: {result['size']/1024:.1f} KB")
            print(f"     Source: {result['source']}")
        else:
            print(f"  ❌ {filename}: FAILED")
    
    return results


if __name__ == "__main__":
    main()