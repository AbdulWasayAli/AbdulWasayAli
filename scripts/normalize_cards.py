import re
from pathlib import Path

def normalize_top_langs(path):
    p = Path(path)
    if not p.exists():
        return
    svg_text = p.read_text(encoding="utf-8")
    
    # Standardize dimensions to 467x195 to match github-stats.svg
    svg_text = re.sub(r'width="\d+"', 'width="467"', svg_text, count=1)
    svg_text = re.sub(r'height="\d+"', 'height="195"', svg_text, count=1)
    svg_text = re.sub(r'viewBox="0 0 \d+ \d+"', 'viewBox="0 0 467 195"', svg_text, count=1)
    
    # Background rect size
    svg_text = re.sub(r'width="299"', 'width="466"', svg_text)
    svg_text = re.sub(r'height="99%"', 'height="194"', svg_text)
    
    # Scale progress bar mask from 250 to 417 (417 / 250 = 1.668)
    svg_text = re.sub(r'width="250"', 'width="417"', svg_text)
    
    def scale_rect(match):
        full = match.group(0)
        x_m = re.search(r'x="([0-9.]+)"', full)
        w_m = re.search(r'width="([0-9.]+)"', full)
        if x_m and w_m:
            new_x = round(float(x_m.group(1)) * 1.668, 2)
            new_w = round(float(w_m.group(1)) * 1.668, 2)
            full = re.sub(r'x="[0-9.]+"', f'x="{new_x}"', full, count=1)
            full = re.sub(r'width="[0-9.]+"', f'width="{new_w}"', full, count=1)
        return full

    svg_text = re.sub(r'<rect\s+mask="url\(#rect-mask\)"[^>]+/>', scale_rect, svg_text)
    
    # Space column 2 nicely at x=220
    svg_text = re.sub(r'transform="translate\(150,\s*0\)"', 'transform="translate(220, 0)"', svg_text)
    
    p.write_text(svg_text, encoding="utf-8")

if __name__ == "__main__":
    normalize_top_langs("assets/top-langs.svg")
