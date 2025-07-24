#!/usr/bin/env python3
"""
Enhanced script to center all images in Markdown files using a more robust HTML approach.
"""
import os
import re
from pathlib import Path

# Path to your chapters
chapters_dir = Path('drafts/chapters')

# Regular expression to find image tags
img_pattern = re.compile(r'<img[^>]+src="[^"]+"[^>]*/?>')

def center_image(img_tag):
    """
    Center an image using a more robust HTML approach that GitHub rendering respects.
    """
    # Extract attributes from the image tag
    src_match = re.search(r'src="([^"]+)"', img_tag)
    if not src_match:
        return img_tag  # If no src attribute found, return unchanged
    
    src = src_match.group(1)
    
    # Extract other attributes if present
    alt_match = re.search(r'alt="([^"]*)"', img_tag)
    alt = alt_match.group(1) if alt_match else ""
    
    style_match = re.search(r'style="([^"]*)"', img_tag)
    style = style_match.group(1) if style_match else ""
    
    # If style already exists, add to it; otherwise create new style
    if style:
        if "margin" not in style:
            style += "; margin: 0 auto; display: block;"
    else:
        style = "margin: 0 auto; display: block;"
    
    # Create a new centered image tag
    centered_img = f'<img src="{src}" alt="{alt}" style="{style}" />'
    
    # Wrap in a center tag for maximum compatibility
    return f'<p align="center">{centered_img}</p>'

# Check if chapters directory exists
if not chapters_dir.exists():
    print(f"Warning: Directory {chapters_dir} does not exist.")
    # Use fallback directory if chapters_dir doesn't exist
    chapters_dir = Path('drafts')
    if not chapters_dir.exists():
        print(f"Error: Directory {chapters_dir} does not exist either.")
        exit(1)

# Count for summary
processed = 0
modified = 0

# Process each markdown file in the chapters directory
for md_file in chapters_dir.glob('**/*.md'):
    processed += 1
    print(f"Processing {md_file}")
    try:
        with open(md_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all image tags
        all_matches = list(re.finditer(img_pattern, content))
        if all_matches:
            print(f"Found {len(all_matches)} images in {md_file}")
            for i, match in enumerate(all_matches):
                print(f"  Image {i+1}: {match.group(0)[:50]}...")
        else:
            print(f"  No images found in {md_file}")
        
        # Replace all image tags with centered image tags
        modified_content = content
        for match in re.finditer(img_pattern, content):
            img_tag = match.group(0)
            
            # Check if this image is already in a centering p tag
            start_pos = match.start()
            p_align_start = content.rfind('<p align="center">', 0, start_pos)
            p_align_end = content.find('</p>', start_pos)
            
            # If not already centered, center it
            if p_align_start == -1 or p_align_end == -1 or p_align_start > p_align_end:
                centered_img = center_image(img_tag)
                modified_content = modified_content.replace(img_tag, centered_img, 1)
                print(f"  Centering: {img_tag[:50]}...")
            else:
                print(f"  Already centered: {img_tag[:50]}...")
        
        # Write the modified content back to the file
        if content != modified_content:
            with open(md_file, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            modified += 1
            print(f"✅ Centered images in {md_file}")
        else:
            print(f"ℹ️ No changes needed for {md_file}")
    except Exception as e:
        print(f"❌ Error processing {md_file}: {e}")

# Print summary
print(f"\nSummary: Processed {processed} files, modified {modified} files.")
