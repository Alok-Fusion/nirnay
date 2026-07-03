import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix Grid item
    content = re.sub(r'<Grid item xs={(\d+)} md={(\d+)}>', r'<Grid size={{ xs: \1, md: \2 }}>', content)
    content = re.sub(r'<Grid item xs={(\d+)} lg={(\d+)}>', r'<Grid size={{ xs: \1, lg: \2 }}>', content)
    content = re.sub(r'<Grid item xs={(\d+)} sm={(\d+)} md={(\d+)} key={([^}]+)}>', r'<Grid size={{ xs: \1, sm: \2, md: \3 }} key={\4}>', content)
    content = re.sub(r'<Grid item xs={(\d+)}>', r'<Grid size={{ xs: \1 }}>', content)
    content = re.sub(r'<Grid item xs={(\d+)} sm={(\d+)}>', r'<Grid size={{ xs: \1, sm: \2 }}>', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

src_dir = 'frontend/src'
for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            fix_file(os.path.join(root, file))
