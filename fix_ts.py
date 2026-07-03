import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix Grid item xs={X} -> size={{ xs: X }}
    content = re.sub(r'<Grid item\s+xs={(\d+)}>', r'<Grid size={{ xs: \1 }}>', content)
    content = re.sub(r'<Grid item\s+xs={(\d+)}\s+sm={(\d+)}>', r'<Grid size={{ xs: \1, sm: \2 }}>', content)
    content = re.sub(r'<Grid item\s+xs={(\d+)}\s+md={(\d+)}>', r'<Grid size={{ xs: \1, md: \2 }}>', content)
    content = re.sub(r'<Grid item\s+xs={(\d+)}\s+lg={(\d+)}>', r'<Grid size={{ xs: \1, lg: \2 }}>', content)
    content = re.sub(r'<Grid item\s+xs={(\d+)}\s+sm={(\d+)}\s+md={(\d+)}\s+key={([^}]+)}>', r'<Grid size={{ xs: \1, sm: \2, md: \3 }} key={\4}>', content)
    
    # Fix Typography fontWeight
    content = re.sub(r'fontWeight="([^"]+)"', r'sx={{ fontWeight: "\1" }}', content)
    content = re.sub(r'fontWeight={([^}]+)}', r'sx={{ fontWeight: \1 }}', content)
    
    # Fix multiple sx={{...}} sx={{...}} which might occur from replacing fontWeight
    content = re.sub(r'sx={{([^}]+)}}\s+sx={{([^}]+)}}', r'sx={{ \1, \2 }}', content)
    
    # Fix TextField InputProps
    if 'TransactionsHub.tsx' in filepath:
        content = content.replace('InputProps={{', 'slotProps={{ input: {')
        content = content.replace('startAdornment: <InputAdornment position="start"><Search /></InputAdornment>,', 'startAdornment: <InputAdornment position="start"><Search /></InputAdornment>')
        content = content.replace('}}\n            sx={{ bgcolor: \'white\', borderRadius: 1 }}', '}}}\n            sx={{ bgcolor: \'white\', borderRadius: 1 }}')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

src_dir = 'frontend/src'
for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            fix_file(os.path.join(root, file))
