#!/usr/bin/env python3
"""
Enhanced script to center all images in Markdown files.
"""
import os
import re
from pathlib import Path

# Path to your chapters
chapters_dir = Path('drafts/chapters')

# More comprehensive pattern to catch various image tag formats
img_pattern = re.compile(r'<img\s+[^>]*src="[^"]+"\s*[^>]*/?>|!\[[^\]]*\]\([^)]+\)')

def center_image(match):
    """Wrap the image in a centered div."""
    img_tag = match.group(0)
    
    # Check if it's a Markdown image ![alt](src) 
    if img_tag.startswith('!'):
        # Convert Markdown to HTML first
        alt_text = re.search(r'!\[(.*?)\]', img_tag)
        alt = alt_text.group(1) if alt_text else ""
        src = re.search(r'\((.*?)\)', img_tag).group(1)
        img_tag = f'<img src="{src}" alt="{alt}" />'
    
    # Make sure the image tag ends properly
    if not img_tag.endswith('/>') and not img_tag.endswith('>'):
        img_tag = img_tag.rstrip('>') + '/>'
    
    return f'<div style="text-align: center;">{img_tag}</div>'

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
        
        # Debug: Print all image tags found
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
            # Check if this image is already in a centering div
            start_pos = match.start()
            div_start = content.rfind('<div style="text-align: center;">', 0, start_pos)
            div_end = content.find('</div>', start_pos)
            
            # If not already centered, center it
            if div_start == -1 or div_end == -1 or div_start > div_end:
                centered_img = f'<div style="text-align: center;">{img_tag}</div>'
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
