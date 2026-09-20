from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path('/mnt/data/n12work')

# Distinct soft colours; six are enough for the largest non-calendar page.
PALETTE = [
    '#f6c8d9',  # rose
    '#c9e8e8',  # aqua
    '#f5e3a5',  # warm yellow
    '#cfe7b9',  # green
    '#d9cce9',  # lavender
    '#f2d0b2',  # peach
    '#cfdcf0',  # blue-lilac
    '#ead5c4',  # tan
]

for path in sorted(ROOT.glob('*.html')):
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    body = soup.body
    if body is None:
        continue
    classes = set(body.get('class') or [])
    is_calendar = 'calendar-page' in classes

    # The image belongs directly between the long page-heading rule and the main
    # content/shorter section rule. Put it in a dedicated band immediately after
    # the page heading on every non-calendar page.
    if not is_calendar:
        page_heading = soup.select_one('.page-heading')
        photo = soup.select_one('.section-photo')
        if page_heading and photo:
            # Reuse the existing image node and detach it from wherever it was.
            band = soup.new_tag('div')
            band['class'] = ['section-photo-band']
            band.append(photo.extract())
            page_heading.insert_after(band)

        # Assign an explicit page-local colour class to every content box.
        # This makes colours distinct within each page irrespective of the
        # original .pink/.teal/.yellow/.green classes.
        boxes = soup.select('.card, .panel, .notice, .quote')
        for i, box in enumerate(boxes):
            # remove earlier generated box colour classes if re-running
            old = [c for c in box.get('class', []) if c.startswith('page-box-')]
            if old:
                box['class'] = [c for c in box.get('class', []) if not c.startswith('page-box-')]
            box['class'] = box.get('class', []) + [f'page-box-{(i % len(PALETTE)) + 1}']

    # Repair the malformed Home body class while we're editing the file.
    # BeautifulSoup normalises it to the intended class token.
    if path.name == 'index.html':
        body['class'] = ['home-page']

    path.write_text(str(soup), encoding='utf-8')

# Add final CSS overrides at the end so they win over the earlier refinement rules.
css = ROOT / 'styles.css'
text = css.read_text(encoding='utf-8')
marker = '/* Final user-requested layout and per-page box colours */'
if marker not in text:
    additions = r'''

/* Final user-requested layout and per-page box colours */
.section-photo-band{
  max-width:var(--max);
  height:174px;
  margin:0 auto;
  padding:0 20px;
  position:relative;
}
.section-photo-band .section-photo{
  position:absolute;
  top:10px;
  right:20px;
  width:128px;
  height:164px;
  margin:0;
  border:3px solid var(--ink);
  box-shadow:6px 6px 0 var(--ink);
  background:var(--yellow);
  overflow:hidden;
}
.section-photo-band .section-photo img{
  display:block;
  width:100%;
  height:100%;
  object-fit:cover;
}
.section-head{
  min-height:0;
  padding-right:0;
}
/* Each page gets a non-repeating sequence of box colours. Calendar is intentionally untouched. */
body:not(.calendar-page) .page-box-1{background:#f6c8d9 !important}
body:not(.calendar-page) .page-box-2{background:#c9e8e8 !important}
body:not(.calendar-page) .page-box-3{background:#f5e3a5 !important}
body:not(.calendar-page) .page-box-4{background:#cfe7b9 !important}
body:not(.calendar-page) .page-box-5{background:#d9cce9 !important}
body:not(.calendar-page) .page-box-6{background:#f2d0b2 !important}
body:not(.calendar-page) .page-box-7{background:#cfdcf0 !important}
body:not(.calendar-page) .page-box-8{background:#ead5c4 !important}
@media(max-width:800px){
  .section-photo-band{height:150px;padding:0 20px}
  .section-photo-band .section-photo{top:8px;right:20px;width:112px;height:140px;box-shadow:4px 4px 0 var(--ink)}
}
'''
    css.write_text(text + additions, encoding='utf-8')
