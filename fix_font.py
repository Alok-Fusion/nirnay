import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match <Typography ... fontWeight="500" ...> -> <Typography ... sx={{ fontWeight: 500 }} ...>
    content = re.sub(r'fontWeight="([^"]+)"', r'sx={{ fontWeight: "\1" }}', content)
    content = re.sub(r'fontWeight={(\d+)}', r'sx={{ fontWeight: \1 }}', content)
    
    # Merge multiple sx tags created by replacing
    content = re.sub(r'sx={{([^}]+)}}\s+sx={{([^}]+)}}', r'sx={{ \1, \2 }}', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

src_dir = 'frontend/src'
for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            fix_file(os.path.join(root, file))
