import os
import re
import shutil

# --- Paths ---
obsidian_posts_dir = r"C:\Users\zacha\Documents\mypi\posts"
attachments_dir = r"C:\Users\zacha\Documents\mypi\Attachments"
hugo_content_dir = r"C:\Users\zacha\Documents\itblog\content\posts" 
hugo_static_images_dir = r"C:\Users\zacha\Documents\itblog\static\images"

# Create target directories if they don't exist
os.makedirs(hugo_content_dir, exist_ok=True)
os.makedirs(hugo_static_images_dir, exist_ok=True)

# --- Processing ---
for filename in os.listdir(obsidian_posts_dir):
    if filename.endswith(".md"):
        obsidian_file = os.path.join(obsidian_posts_dir, filename)
        hugo_file = os.path.join(hugo_content_dir, filename)
        
        with open(obsidian_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Regex to find either:
        # 1. ![Alt](Attachments/image.png)
        # 2. [[Attachments/image.png]]
        # 3. [[image.png]]
        def replace_link(match):
            # Extract the full path captured in the match
            full_path = match.group(1)
            # Get just the filename (remove 'Attachments/' if it's there)
            img_name = os.path.basename(full_path)
            
            # Copy file to Hugo static folder
            src = os.path.join(attachments_dir, img_name)
            if os.path.exists(src):
                shutil.copy2(src, hugo_static_images_dir)
            
            # Return the Hugo-ready markdown link
            return f"![Image Description](/images/{img_name.replace(' ', '%20')})"

        # Apply replacements
        # Matches: ![alt](path) or [[path]]
        content = re.sub(r'!\[.*?\]\((?:Attachments/)?([^)]+\.png)\)', replace_link, content)
        content = re.sub(r'\[\[(?:Attachments/)?([^\]]+\.png)\]\]', replace_link, content)
        
        # Write to the Hugo directory
        with open(hugo_file, "w", encoding="utf-8") as f:
            f.write(content)

print("Sync complete: Files copied to Hugo and links normalized to /images/.")