#!/usr/bin/env python3
"""
Generate a Rio Tinto corporate-branded PDF from any markdown file.

Usage:
  python3 generate_pdf.py --input doc.md [--output doc.pdf] [--title "My Title"]
                          [--subtitle "Subtitle"] [--prepared-by "Team"]
                          [--classification "CONFIDENTIAL"] [--scope "Scope line"]
                          [--date "16 March 2026"]
"""
import argparse
import os
import re
import sys
import datetime

# ── Rio Tinto brand colours (extracted from reference PDF drawings) ─────────
RT_RED      = "#CD2C2C"   # RGB(205,44,44) — exact from PDF fill data
RT_BLACK    = "#000000"
RT_TITLE    = "#262626"   # near-black title text from cover page
RT_GREY     = "#7F7F7F"   # grey copyright text on cover
RT_BODY     = "#000000"   # body text
RT_BORDER   = "#C0C0C0"   # table borders
RT_LIGHT    = "#F2F2F2"   # table alternating rows
RT_ACCENT   = "#CD2C2C"   # same red for any accent use


# ── HTML/CSS template ─────────────────────────────────────────────────────
CSS = f"""
/* ── Page layout ── */
@page {{
    size: A4;
    /* Top margin: header sits at top, leaving ~12mm of air before content */
    margin: 28mm 20mm 28mm 20mm;

    /* Single @top-left spans full width (no @top-center / @top-right) */
    @top-left {{
        content: element(rt-header);
        vertical-align: top;
        padding-top: 5mm;
    }}
    @top-center {{ content: none; }}
    @top-right  {{ content: none; }}

    /* Footer: no rule, lighter text — center for content, right for page number */
    @bottom-left   {{ content: none; }}
    @bottom-center {{
        content: element(rt-footer);
        vertical-align: top;
    }}
    @bottom-right {{
        content: counter(page) " / " counter(pages);
        font-family: Arial, sans-serif;
        font-size: 7pt;
        color: {RT_GREY};
        vertical-align: top;
        padding-top: 4pt;
        text-align: right;
        width: 20mm;
    }}
}}

/* Cover page — no running headers/footers, no margins */
@page :first {{
    margin: 0;
    @top-left      {{ content: none; }}
    @top-center    {{ content: none; }}
    @top-right     {{ content: none; }}
    @bottom-left   {{ content: none; border-top: none; }}
    @bottom-center {{ content: none; border-top: none; }}
    @bottom-right  {{ content: none; border-top: none; }}
}}

/* ── Running header — explicit content-area width so float: right works ── */
#rt-header {{
    position: running(rt-header);
    width: 170mm;
    border-bottom: 0.75pt solid {RT_BLACK};
    padding-bottom: 3pt;
    overflow: hidden;
}}

/* Logo floated right; text fills the left */
.rt-hdr-right {{
    float: right;
    line-height: 1;
}}

.rt-hdr-right img {{
    height: 10pt;
    width: auto;
    display: block;
}}

.rt-hdr-left {{
    font-family: Arial, sans-serif;
    font-size: 7pt;
    color: {RT_BLACK};
    line-height: 2.2;
    overflow: hidden;
}}

/* Override general table styles inside the running header */
#rt-header table {{
    border: none;
    margin: 0;
}}
#rt-header td {{
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}}

/* ── Running footer element — no rule, light grey so it reads as footer ── */
#rt-footer {{
    position: running(rt-footer);
    font-family: Arial, sans-serif;
    font-size: 7.5pt;
    color: {RT_GREY};
    text-align: center;
    padding-top: 4pt;
    width: 100%;
}}

/* ── Base styles ── */
* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    font-family: Arial, sans-serif;
    font-size: 10pt;
    color: {RT_BODY};
    line-height: 1.5;
    background: white;
}}

/* ══════════════════════════════
   COVER PAGE
══════════════════════════════ */
.cover {{
    width: 210mm;
    height: 297mm;
    padding: 20mm 20mm 18mm 20mm;
    page-break-after: always;
    position: relative;
    background: white;
}}

.cover-logo {{
    display: block;
    margin-bottom: 22mm;
    line-height: 1;
}}

.cover-logo img, .cover-logo svg {{
    height: 7mm;
    width: auto;
}}

.cover-title {{
    font-family: Arial, sans-serif;
    font-size: 28pt;
    font-weight: bold;
    color: {RT_TITLE};
    line-height: 1.15;
    margin-bottom: 12mm;
}}

.cover-date {{
    font-family: Arial, sans-serif;
    font-size: 14pt;
    font-weight: normal;
    color: {RT_BLACK};
    margin-bottom: 0;
}}

.cover-footer {{
    position: absolute;
    bottom: 18mm;
    left: 20mm;
}}

.cover-footer p {{
    font-family: Arial, sans-serif;
    font-size: 9pt;
    color: {RT_GREY};
    line-height: 1.5;
    margin: 0;
}}

/* ══════════════════════════════
   MAIN CONTENT
══════════════════════════════ */
.content {{
    /* content area — margins handled by @page */
}}

/* ── Section page break wrapper (every section, including first, starts on new page) ── */
.section {{
    page-break-before: always;
}}

/* ── h2 — main section heading, 16pt bold + thin rule below ── */
h2 {{
    font-family: Arial, sans-serif;
    font-size: 16pt;
    font-weight: bold;
    color: {RT_BLACK};
    margin: 0 0 12pt 0;
    padding: 0 0 6pt 0;
    border-bottom: 1pt solid {RT_BLACK};
    page-break-after: avoid;
}}

/* ── h3 — sub-heading, 14pt bold ── */
h3 {{
    font-family: Arial, sans-serif;
    font-size: 14pt;
    font-weight: bold;
    color: {RT_BLACK};
    margin: 16pt 0 7pt 0;
    padding: 0;
    page-break-after: avoid;
}}

/* ── h4 — minor heading, 10pt bold ── */
h4 {{
    font-family: Arial, sans-serif;
    font-size: 10pt;
    font-weight: bold;
    color: {RT_BLACK};
    margin: 12pt 0 5pt 0;
    page-break-after: avoid;
}}

p {{
    margin: 0 0 8pt 0;
    font-size: 10pt;
    color: {RT_BODY};
}}

strong {{ font-weight: bold; }}
em {{ font-style: italic; }}

/* ── Tables — clean simple borders, first column bold ── */
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12pt 0 16pt 0;
    font-size: 9.5pt;
    page-break-inside: auto;
}}

/* Repeat header row on every page when table spans multiple pages */
thead {{
    display: table-header-group;
}}

thead tr {{
    background: white;
}}

thead th {{
    padding: 7pt 9pt;
    text-align: left;
    font-weight: bold;
    font-size: 9.5pt;
    border: 0.75pt solid {RT_BORDER};
    border-bottom: 1.5pt solid {RT_BLACK};
    color: {RT_BLACK};
    background: white;
}}

tbody tr:nth-child(even) {{
    background: {RT_LIGHT};
}}

tbody tr:nth-child(odd) {{
    background: white;
}}

tbody td {{
    padding: 6pt 9pt;
    border: 0.75pt solid {RT_BORDER};
    vertical-align: top;
    color: {RT_BODY};
    font-size: 9.5pt;
}}

tbody td:first-child {{
    font-weight: bold;
}}

/* ── Inline code ── */
code {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 8.5pt;
    background: {RT_LIGHT};
    padding: 1pt 3pt;
    border: 0.5pt solid {RT_BORDER};
    color: {RT_BLACK};
}}

/* ── Code block ── */
pre {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 8pt;
    background: {RT_LIGHT};
    border: 0.75pt solid {RT_BORDER};
    padding: 7pt 9pt;
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 5pt 0 8pt 0;
    color: {RT_BLACK};
    page-break-inside: avoid;
}}

/* ── Blockquote — left-border callout ── */
blockquote {{
    border-left: 3pt solid {RT_RED};
    padding: 4pt 10pt;
    margin: 5pt 0 8pt 0;
    font-size: 9.5pt;
    color: #333;
    font-style: italic;
}}

blockquote p {{ margin: 0; }}

/* ── Lists ── */
ul, ol {{
    margin: 4pt 0 9pt 20pt;
    padding: 0;
}}

li {{
    margin: 3pt 0;
    font-size: 10pt;
}}

/* ── HR ── */
hr {{
    border: none;
    border-top: 0.5pt solid {RT_BORDER};
    margin: 12pt 0;
}}

/* ── Urgency / status badges ── */
.badge-red    {{ color: #CC0000; font-weight: bold; }}
.badge-orange {{ color: #CC5500; font-weight: bold; }}
.badge-yellow {{ color: #886600; font-weight: bold; }}
.badge-green  {{ color: #007700; font-weight: bold; }}

/* ── TOC hyperlinks — no underline, black text, hover-style via color ── */
a.toc-link {{
    display: block;
    text-decoration: none;
    color: {RT_BLACK};
}}

a.toc-link:hover {{
    color: {RT_RED};
}}

.toc-item {{
    display: flex;
    align-items: baseline;
    padding: 5pt 0;
    border-bottom: 0.5pt dotted {RT_BORDER};
}}

.toc-item-section {{
    font-size: 9pt;
    color: {RT_GREY};
    min-width: 12mm;
    flex-shrink: 0;
}}

.toc-item-title {{
    font-size: 10pt;
    flex: 1;
}}

.toc-item-title:hover {{
    color: {RT_RED};
}}

/* ── Document Control / cover metadata table ── */
.meta-table {{
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0;
    font-size: 10pt;
}}

.meta-table td {{
    padding: 4pt 6pt 4pt 0;
    border-bottom: 0.5pt solid {RT_BORDER};
    vertical-align: top;
}}

.meta-table td:first-child {{
    font-weight: bold;
    width: 42mm;
    color: {RT_BLACK};
}}

/* ── Change log table ── */
.changelog-table {{
    border-collapse: collapse;
    width: 100%;
    margin: 6pt 0;
    font-size: 9.5pt;
}}

.changelog-table th {{
    font-weight: bold;
    border: 0.75pt solid {RT_BORDER};
    padding: 4pt 6pt;
    text-align: left;
    background: white;
}}

.changelog-table td {{
    padding: 3pt 6pt;
    border: 0.75pt solid {RT_BORDER};
}}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<style>{css}</style>
</head>
<body>

<!-- ── Running header: logo floated right, doc title fills left ── -->
<div id="rt-header">
  <span class="rt-hdr-right">{logo_html_hdr}</span>
  <span class="rt-hdr-left">{doc_title_short}</span>
</div>

<!-- ── Running footer ── -->
<div id="rt-footer">
  {doc_title_short}<br/>
  {classification}
</div>

<!-- ══════════════════════════════════════════
     COVER PAGE  (full-bleed, no page margins)
══════════════════════════════════════════ -->
<div class="cover">

  <!-- RioTinto logo (SVG wordmark) -->
  <div class="cover-logo">{logo_html}</div>

  <!-- Document title -->
  <div class="cover-title">{title_html}</div>

  <!-- Date -->
  <div class="cover-date">{date}</div>

  <!-- Bottom-left: copyright / classification lines -->
  <div class="cover-footer">
    <p>&#169; {year}, Held within Rio Tinto</p>
    <p>For Internal Use Only</p>
    <p>{classification}</p>
  </div>

</div>

<!-- ══════════════════════════════════════════
     DOCUMENT CONTROL PAGE
══════════════════════════════════════════ -->
<div class="section">
<h2>Document Control</h2>

<table class="meta-table">
  <tr><td>Document Name</td><td>{title_html}</td></tr>
  <tr><td>Document Status</td><td>Draft</td></tr>
  <tr><td>Version No.</td><td>0.1</td></tr>
  <tr><td>Prepared By</td><td>{prepared_by}</td></tr>
  <tr><td>Date</td><td>{date}</td></tr>{extra_meta_rows}
</table>
</div>

<!-- ══════════════════════════════════════════
     CHANGE LOG PAGE
══════════════════════════════════════════ -->
<div class="section">
<h2>Change Log</h2>
<table class="changelog-table">
  <thead><tr><th>Version</th><th>Date</th><th>Prepared by</th><th>Description of Changes</th></tr></thead>
  <tbody>
    <tr><td>0.1</td><td>{date}</td><td>{prepared_by}</td><td>Initial draft</td></tr>
  </tbody>
</table>
</div>

{body}

</body>
</html>
"""


def slugify(text: str) -> str:
    """Convert a heading title to a URL-safe anchor ID."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text).strip('-')
    return text


def md_table_to_html(block: str) -> str:
    """Convert a markdown table block to an HTML table."""
    lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
    # Remove separator lines (---|---)
    rows = [l for l in lines if not re.match(r'^[\|\s\-:]+$', l)]
    if not rows:
        return ""

    html = "<table>\n"
    for i, row in enumerate(rows):
        cells = [c.strip() for c in row.strip('|').split('|')]
        tag = "th" if i == 0 else "td"
        wrap = "thead" if i == 0 else ("tbody" if i == 1 else "")
        if i == 0:
            html += "<thead><tr>"
        elif i == 1:
            html += "</thead>\n<tbody>\n<tr>"
        else:
            html += "<tr>"
        for cell in cells:
            cell = inline_md(cell)
            html += f"<{tag}>{cell}</{tag}>"
        html += "</tr>\n"
    html += "</tbody>\n</table>\n"
    return html


def inline_md(text: str) -> str:
    """Convert inline markdown to HTML."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    # Emoji-like urgency markers in tables
    text = text.replace('🔴', '<span class="badge-red">●</span>')
    text = text.replace('🟠', '<span class="badge-orange">●</span>')
    text = text.replace('🟡', '<span class="badge-yellow">●</span>')
    text = text.replace('✅', '✓')
    text = text.replace('❌', '✗')
    return text


def md_to_html_body(md: str) -> str:
    """Convert the stage1_reports.md content to styled HTML body."""
    lines = md.splitlines()
    html_parts = []
    i = 0
    in_code = False
    code_buf = []
    in_list = False
    list_type = None
    report_count = 0
    appendix_count = 0

    # Track table accumulation
    table_buf = []
    in_table = False

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            tag = "ul" if list_type == "ul" else "ol"
            html_parts.append(f"</{tag}>\n")
            in_list = False
            list_type = None

    def flush_table():
        nonlocal in_table, table_buf
        if in_table and table_buf:
            html_parts.append(md_table_to_html("\n".join(table_buf)))
            table_buf = []
            in_table = False

    while i < len(lines):
        line = lines[i]

        # Code fence — handles both flush and indented fences (e.g. "   ```")
        if line.strip().startswith("```"):
            if in_code:
                code_content = "\n".join(code_buf)
                html_parts.append(f"<pre>{code_content}</pre>\n")
                code_buf = []
                in_code = False
            else:
                flush_list()
                flush_table()
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Table detection
        if '|' in line and line.strip().startswith('|'):
            flush_list()
            in_table = True
            table_buf.append(line)
            i += 1
            continue
        elif in_table:
            flush_table()

        # Skip the raw title (first h1)
        if line.startswith("# ") and not line.startswith("## "):
            i += 1
            continue

        # h2 — every ## heading starts a new page section
        if line.startswith("## "):
            flush_list()
            title = line[3:].strip()
            anchor = slugify(title)
            html_parts.append(f'<div class="section">\n<h2 id="{anchor}">{inline_md(title)}</h2>\n')
            i += 1
            continue

        # h3
        if line.startswith("### "):
            flush_list()
            title = line[4:].strip()
            html_parts.append(f"<h3>{inline_md(title)}</h3>\n")
            i += 1
            continue

        # h4
        if line.startswith("#### "):
            flush_list()
            title = line[5:].strip()
            html_parts.append(f"<h4>{inline_md(title)}</h4>\n")
            i += 1
            continue

        # HR
        if re.match(r'^---+$', line.strip()):
            flush_list()
            html_parts.append("<hr/>\n")
            i += 1
            continue

        # Blockquote
        if line.startswith("> "):
            flush_list()
            content = inline_md(line[2:])
            html_parts.append(f"<blockquote><p>{content}</p></blockquote>\n")
            i += 1
            continue

        # Unordered list
        if re.match(r'^[\-\*\+] ', line):
            if not in_list or list_type != "ul":
                if in_list:
                    flush_list()
                html_parts.append("<ul>\n")
                in_list = True
                list_type = "ul"
            content = inline_md(line[2:])
            html_parts.append(f"<li>{content}</li>\n")
            i += 1
            continue

        # Ordered list
        if re.match(r'^\d+\. ', line):
            if not in_list or list_type != "ol":
                if in_list:
                    flush_list()
                html_parts.append("<ol>\n")
                in_list = True
                list_type = "ol"
            content = inline_md(re.sub(r'^\d+\. ', '', line))
            html_parts.append(f"<li>{content}</li>\n")
            i += 1
            continue

        flush_list()

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Regular paragraph
        html_parts.append(f"<p>{inline_md(line)}</p>\n")
        i += 1

    flush_list()
    flush_table()

    return "".join(html_parts)


def build_toc_from_md(md_content: str) -> str:
    """Auto-generate a hyperlinked table of contents from ## headings in the markdown."""
    entries = []
    for line in md_content.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            m = re.match(r'^(Report\s+\d+|Appendix\s+[A-Z])', title)
            if m:
                label = m.group(1).replace("Report ", "").replace("Appendix ", "")
            else:
                label = "—"
            entries.append((label, title, slugify(title)))

    if not entries:
        return ""

    rows = ""
    for label, title, anchor in entries:
        rows += f"""
    <a class="toc-link" href="#{anchor}">
      <div class="toc-item">
        <span class="toc-item-section">{label}</span>
        <span class="toc-item-title"><strong>{inline_md(title)}</strong></span>
      </div>
    </a>"""

    return f"""
<div class="section">
  <h2>Contents</h2>
  <div class="toc-body">{rows}
  </div>
</div>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Rio Tinto branded PDF from a markdown file."
    )
    parser.add_argument("--input",   required=True,  help="Source markdown file path")
    parser.add_argument("--output",  default=None,   help="Output PDF path (default: input with .pdf)")
    parser.add_argument("--title",   default=None,   help="Cover page main title")
    parser.add_argument("--subtitle",default="",     help="Cover page subtitle")
    parser.add_argument("--prepared-by", default="Network Platform Team", help="Prepared by field")
    parser.add_argument("--classification", default="CONFIDENTIAL — INTERNAL USE ONLY",
                        help="Cover banner and footer classification text")
    parser.add_argument("--scope",   default="",     help="Scope line for cover metadata")
    parser.add_argument("--date",    default=None,   help="Override document date")
    args = parser.parse_args()

    src = os.path.abspath(args.input)
    if not os.path.exists(src):
        print(f"ERROR: Input file not found: {src}", file=sys.stderr)
        sys.exit(1)

    out = args.output or os.path.splitext(src)[0] + ".pdf"
    out = os.path.abspath(out)

    with open(src, "r") as f:
        md_content = f.read()

    # Infer title from first # heading if not provided
    title = args.title
    if not title:
        for line in md_content.splitlines():
            if line.startswith("# ") and not line.startswith("## "):
                title = line[2:].strip()
                break
        if not title:
            title = os.path.splitext(os.path.basename(src))[0].replace("_", " ").replace("-", " ")

    today = args.date or datetime.date.today().strftime("%-d %B %Y")
    prepared_by = args.prepared_by
    classification = args.classification
    subtitle = args.subtitle
    scope = args.scope

    # Build cover title HTML (support \n line breaks)
    title_html = title.replace("\n", "<br/>")

    # Short doc title for running header/footer (truncate if needed)
    doc_title_short = title if len(title) <= 90 else title[:87] + "…"

    # Extra metadata rows for document control page
    extra_meta_rows = ""
    if scope:
        extra_meta_rows += f"\n  <tr><td>Scope</td><td>{scope}</td></tr>"
    if subtitle:
        extra_meta_rows += f"\n  <tr><td>Description</td><td>{subtitle}</td></tr>"

    # Build TOC from markdown headings
    toc_html = build_toc_from_md(md_content)

    # Convert markdown body to HTML
    body_html = toc_html + md_to_html_body(md_content)

    year = datetime.date.today().year

    # Load logo SVG — look in assets/ (sibling of scripts/), then beside the input file
    logo_html = ""
    logo_svg_raw = ""
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for logo_candidate in [
        os.path.join(skill_root, "assets", "logo.svg"),
        os.path.join(os.path.dirname(src), "logo.svg"),
    ]:
        if os.path.exists(logo_candidate):
            with open(logo_candidate, "r") as f:
                logo_svg_raw = f.read()
            logo_html = logo_svg_raw
            break
    if not logo_html:
        logo_html = f'<span style="font-family:Arial;font-weight:bold;font-size:20pt;color:{RT_RED};letter-spacing:-0.5pt;">RioTinto</span>'

    # Header logo: base64 <img> — height controlled reliably via CSS
    import base64 as _b64
    if logo_svg_raw:
        _enc = _b64.b64encode(logo_svg_raw.encode("utf-8")).decode("ascii")
        logo_html_hdr = f'<img src="data:image/svg+xml;base64,{_enc}" />'
    else:
        logo_html_hdr = '<span style="font-family:Arial;font-weight:bold;font-size:10pt;color:#CD2C2C;">RioTinto</span>'

    full_html = HTML_TEMPLATE.format(
        css=CSS,
        body=body_html,
        date=today,
        year=year,
        prepared_by=prepared_by,
        title_html=title_html,
        doc_title_short=doc_title_short,
        classification=classification,
        extra_meta_rows=extra_meta_rows,
        logo_html=logo_html,
        logo_html_hdr=logo_html_hdr,
    )

    # Write debug HTML for inspection
    debug_html = os.path.join("/tmp", os.path.splitext(os.path.basename(src))[0] + "_debug.html")
    with open(debug_html, "w") as f:
        f.write(full_html)

    from weasyprint import HTML
    import warnings
    warnings.filterwarnings("ignore")

    print(f"Generating PDF: {out}")
    HTML(string=full_html).write_pdf(out)
    print(f"Done — PDF written to: {out}")


if __name__ == "__main__":
    main()
