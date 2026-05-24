#!/usr/bin/env python3
"""
Search for free-to-use images on Unsplash, Pexels, and Pixabay
and download the highest-resolution versions.
"""

import os
import re
import json
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = "/home/alexagent/projects/gas-inpex-site/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ============================================================
# Query strings for each image we need
# ============================================================
SEARCH_QUERIES = {
    "obj-boiler-house.jpg": "industrial boiler room factory boiler equipment pipes steel",
    "obj-automation.jpg": "factory automation control room industrial control panels PLC SCADA",
    "obj-cottage.jpg": "modern smart home luxury cottage exterior architecture",
    "obj-pipeline.jpg": "gas pipeline industrial pipeline installation large steel pipes construction",
}

# ============================================================
# Unsplash scraper
# ============================================================
def search_unsplash(query, max_results=5):
    """Search Unsplash and return list of (image_url, page_url, description)"""
    encoded = urllib.parse.quote(query)
    url = f"https://unsplash.com/s/photos/{encoded}"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  Unsplash search failed: {e}")
        return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    
    # Look for figure/img elements with the image data
    # Unsplash uses specific data attributes or src sets
    for img in soup.select("img[src*='images.unsplash.com']"):
        src = img.get("src", "")
        if not src or "avatar" in src or "profile" in src:
            continue
        
        # Get the alt text for description
        alt = img.get("alt", "") or ""
        
        # Get parent link for page URL
        parent_link = img.find_parent("a")
        page_url = ""
        if parent_link:
            href = parent_link.get("href", "")
            if href and not href.startswith("http"):
                href = "https://unsplash.com" + href
            page_url = href
        
        # Only add if src looks like a real photo
        if "/photo-" in src or "unsplash.com/photo/" in src:
            results.append((src, page_url, alt))
            if len(results) >= max_results:
                break
    
    # Also try to get from JSON-LD or from data attributes
    if not results:
        # Try to find images from search results more directly
        for img in soup.select("figure img, img[data-test='photo-grid-masonry-img'], img[src*='unsplash']"):
            src = img.get("src", "") or img.get("data-src", "") or ""
            if "images.unsplash.com" in src and "avatar" not in src and "profile" not in src:
                alt = img.get("alt", "") or ""
                # Get the highest res by replacing params
                results.append((src, "", alt))
                if len(results) >= max_results:
                    break
    
    return results


def get_unsplash_download_url(image_url):
    """Convert an Unsplash image URL to a high-resolution download URL.
    Unsplash URLs have format: https://images.unsplash.com/photo-XXXX?w=XXX&...
    We want the raw/full size version.
    """
    # Strip query params and add raw quality
    base = image_url.split("?")[0]
    # For raw/original
    return f"{base}?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1920&fit=max"


# ============================================================
# Pexels scraper
# ============================================================
def search_pexels(query, max_results=5):
    """Search Pexels and return list of (image_url, page_url, description)"""
    encoded = urllib.parse.quote(query)
    url = f"https://www.pexels.com/search/{encoded}/"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  Pexels search failed: {e}")
        return []
    
    results = []
    
    # Pexels uses article/image tags in search results
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Find all img elements that are actual photo results
    for img in soup.select("article img, img[src*='pexels.com/photo/']"):
        src = img.get("src", "") or img.get("data-src", "") or ""
        if not src or "logo" in src or "icon" in src:
            continue
        if "pexels.com/photo/" in src or "images.pexels.com" in src:
            alt = img.get("alt", "") or ""
            results.append((src, "", alt))
            if len(results) >= max_results:
                break
    
    # If no results, try alternative selectors
    if not results:
        for img in soup.select("img[loading='lazy']"):
            src = img.get("src", "") or img.get("data-src", "") or ""
            if "images.pexels.com" in src:
                alt = img.get("alt", "") or ""
                results.append((src, "", alt))
                if len(results) >= max_results:
                    break
    
    return results


def get_pexels_download_url(image_url):
    """Get a high-res version from a Pexels image URL.
    Pexels URLs: https://images.pexels.com/photos/XXXXX/XXX.jpeg?auto=compress&cs=tinysrgb&w=XXX
    We can just change the width parameter or use the original.
    """
    # Remove query params and add original quality
    base = image_url.split("?")[0]
    # Pexels original: remove the compression params
    # The original can be fetched with ?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2
    return f"{base}?auto=compress&cs=tinysrgb&w=1920&h=1080&fit=crop"


# ============================================================
# Pixabay scraper
# ============================================================
def search_pixabay(query, max_results=5):
    """Search Pixabay and return list of (image_url, page_url, description)"""
    encoded = urllib.parse.quote(query)
    url = f"https://pixabay.com/images/search/{encoded}/"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  Pixabay search failed: {e}")
        return []
    
    results = []
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Pixabay uses a specific structure with lazy-loaded images
    for img in soup.select("img[src*='pixabay.com'], img[data-lazy-src*='pixabay.com']"):
        src = img.get("src", "") or img.get("data-lazy-src", "") or ""
        if not src or "logo" in src or "avatar" in src:
            continue
        if "pixabay.com" in src:
            alt = img.get("alt", "") or ""
            results.append((src, "", alt))
            if len(results) >= max_results:
                break
    
    # Try another selector pattern
    if not results:
        for div in soup.select("div[class*='item'] img, a[class*='item'] img"):
            src = div.get("src", "") or div.get("data-lazy-src", "") or ""
            if "pixabay.com" in src and "logo" not in src:
                alt = div.get("alt", "") or ""
                results.append((src, "", alt))
                if len(results) >= max_results:
                    break
    
    return results


def get_pixabay_download_url(image_url):
    """Get a high-res version from a Pixabay image URL.
    Pixabay has different sizes: tiny, small, medium, large, original.
    """
    # Replace size indicators
    # Pixabay URLs often have: https://pixabay.com/get/XXXX_XXXX.jpg
    # or https://cdn.pixabay.com/photo/XXXX/XXXX_XXXX.jpg
    # Try to get the largest version available
    
    # If it's a cdn.pixabay.com URL, we can try to modify the size suffix
    if "cdn.pixabay.com" in image_url:
        # Replace _640.jpg, _1280.jpg, etc. with the original
        # Common patterns: filename_640.jpg, filename_1280.jpg
        # Original is usually without the size suffix
        base, ext = os.path.splitext(image_url)
        # Remove size suffix like _640, _1280, etc.
        base_clean = re.sub(r'_\d+$', '', base)
        return f"{base_clean}{ext}"
    
    return image_url


# ============================================================
# Download and save
# ============================================================
def download_image(url, filepath, source_name="unknown"):
    """Download an image from URL and save to filepath."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        resp.raise_for_status()
        
        content_type = resp.headers.get("Content-Type", "")
        if "image" not in content_type.lower():
            print(f"  WARNING: Not an image! Content-Type: {content_type}")
            return False
        
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        
        size = os.path.getsize(filepath)
        print(f"  Downloaded ({size/1024:.1f} KB): {filepath}")
        return True
    except Exception as e:
        print(f"  Failed to download from {source_name}: {e}")
        return False


def try_alternate_sources(search_func, sources, query, filename, max_per_source=3):
    """Try multiple search sources for a query and download the best result."""
    target_path = os.path.join(OUTPUT_DIR, filename)
    all_candidates = []
    
    for source_name, search_fn in sources:
        print(f"  Searching {source_name} for '{query}'...")
        try:
            results = search_fn(query, max_results=max_per_source)
            for img_url, page_url, desc in results:
                all_candidates.append((source_name, img_url, page_url, desc))
            print(f"    Found {len(results)} results from {source_name}")
        except Exception as e:
            print(f"    Error searching {source_name}: {e}")
        time.sleep(0.5)  # Be polite
    
    if not all_candidates:
        print(f"  NO RESULTS FOUND for {filename}")
        return None
    
    print(f"  Total candidates: {len(all_candidates)}")
    
    # Try each candidate until one downloads successfully
    for source_name, img_url, page_url, desc in all_candidates:
        print(f"  Trying {source_name}: {img_url[:80]}...")
        
        # Get high-res URL based on source
        if "unsplash" in source_name.lower():
            dl_url = get_unsplash_download_url(img_url)
        elif "pexels" in source_name.lower():
            dl_url = get_pexels_download_url(img_url)
        elif "pixabay" in source_name.lower():
            dl_url = get_pixabay_download_url(img_url)
        else:
            dl_url = img_url
        
        if download_image(dl_url, target_path, source_name):
            size = os.path.getsize(target_path)
            return {"path": target_path, "size": size, "source": source_name, "url": dl_url}
        
        time.sleep(0.3)
    
    return None


def main():
    sources = [
        ("Unsplash", search_unsplash),
        ("Pexels", search_pexels),
        ("Pixabay", search_pixabay),
    ]
    
    results = {}
    
    for filename, query in SEARCH_QUERIES.items():
        print(f"\n{'='*60}")
        print(f"SEARCHING: {filename}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        result = try_alternate_sources(None, sources, query, filename)
        if result:
            results[filename] = result
            print(f"  ✅ SUCCESS: {result['path']} ({result['size']/1024:.1f} KB)")
        else:
            results[filename] = None
            print(f"  ❌ FAILED: Could not download {filename}")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for filename, result in results.items():
        if result:
            print(f"  ✅ {filename}: {result['path']} ({result['size']/1024:.1f} KB from {result['source']})")
        else:
            print(f"  ❌ {filename}: FAILED")
    
    return results


if __name__ == "__main__":
    main()