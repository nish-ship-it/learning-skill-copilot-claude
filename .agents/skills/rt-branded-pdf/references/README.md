# rt-branded-pdf — Rio Tinto Branded PDF Generator

Converts any Markdown file into a polished, print-ready A4 PDF using the authentic
Rio Tinto corporate document template. No external services required — runs entirely
locally with Python + WeasyPrint.

---

## Quick Start

```bash
python3 scripts/generate_pdf.py \
  --input  /path/to/your_doc.md \
  --output /path/to/output.pdf \
  --title  "Your Document Title" \
  --prepared-by "Your Team Name" \
  --classification "Commercial in Confidence"
```

Only `--input` is required. All other arguments have sensible defaults.

---

## What the Output Looks Like

| Page | Content                                                                                                          |
| ---- | ---------------------------------------------------------------------------------------------------------------- |
| 1    | **Cover** — RioTinto logo, bold title, date, copyright footer                                                    |
| 2    | **Document Control** — metadata table (name, status, version, date, scope)                                       |
| 3    | **Change Log** — version history table                                                                           |
| 4    | **Contents** — auto-built from all `##` headings; each entry is a **clickable PDF link** jumping to that section |
| 5+   | **Content pages** — each `##` section starts on its own page                                                     |

Every content page has:

- **Header** — doc title left · RioTinto logo right · thin black rule across full width
- **Footer** — doc title + classification centred in light grey · page `N / Total` right

Large tables flow continuously across pages; the column header row repeats automatically at the top of each continuation page.

---

## All Arguments

| Argument           | Required | Default                            | Description                                            |
| ------------------ | -------- | ---------------------------------- | ------------------------------------------------------ |
| `--input`          | ✅       | —                                  | Path to source `.md` file                              |
| `--output`         | No       | Source path + `.pdf`               | Output PDF path                                        |
| `--title`          | No       | First `#` heading in markdown      | Cover page main title                                  |
| `--subtitle`       | No       | _(blank)_                          | Adds a "Description" row to the Document Control table |
| `--prepared-by`    | No       | `Network Platform Team`            | "Prepared By" field on cover                           |
| `--classification` | No       | `CONFIDENTIAL — INTERNAL USE ONLY` | Shown on cover footer and running footer               |
| `--scope`          | No       | _(blank)_                          | Adds a "Scope" row to the Document Control table       |
| `--date`           | No       | Today (`%-d %B %Y`)                | Overrides the document date                            |

---

## Supported Markdown

| Markdown syntax         | Rendered as                                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `# Title`               | Skipped (only used if `--title` is not provided)                                                                                      |
| `## Section`            | Bold h2 with bottom rule; **page break before**; anchor ID auto-generated                                                             |
| `### Sub-section`       | Bold h3                                                                                                                               |
| `#### Minor heading`    | Bold h4                                                                                                                               |
| `\| table \| syntax \|` | Styled table — uniform 0.75pt borders, bold first column, alternating grey rows; large tables flow across pages with repeating header |
| `` `inline code` ``     | Monospace box                                                                                                                         |
| ` ```fenced block``` `  | Grey background pre block (indented fences also supported)                                                                            |
| `> blockquote`          | Left red border callout                                                                                                               |
| `**bold**` / `*italic*` | Bold / Italic                                                                                                                         |
| `- item` / `1. item`    | Unordered / ordered lists                                                                                                             |
| `---`                   | Horizontal rule                                                                                                                       |
| `🔴 🟠 🟡`              | Coloured badge dots in tables                                                                                                         |
| `✅ ❌`                 | ✓ / ✗ symbols                                                                                                                         |

---

## Dependencies

```bash
pip install weasyprint
```

WeasyPrint renders HTML+CSS to PDF. Python 3.10+ required.

To verify a generated PDF (optional):

```bash
python3 -c "from pypdf import PdfReader; r=PdfReader('output.pdf'); print(f'{len(r.pages)} pages')"
# pip install pypdf  ← if not installed
```

---

## Files in This Directory

```
rt-branded-pdf/
├── SKILL.md               ← Copilot agent instructions (do not edit for branding changes)
├── assets/
│   └── logo.svg           ← RioTinto SVG wordmark (used on cover + running header)
├── scripts/
│   └── generate_pdf.py    ← the generator — edit this to change the template
└── references/
    └── README.md          ← you are here
```

---

## How to Customise the Template

All template code lives in `generate_pdf.py`. The file is structured as:

```
1 – Brand colour constants     (lines ~17–25)
2 – CSS block                  (CSS = f"""...""")
3 – HTML template              (HTML_TEMPLATE = """...""")
4 – Markdown parser functions  (md_to_html_body, build_toc_from_md, etc.)
5 – main() entry point
```

### Changing colours

Edit the constants near the top of the file:

```python
RT_RED    = "#CD2C2C"   # Rio Tinto red  — used for logo, h2 underline, blockquote border
RT_BLACK  = "#000000"   # Body text, header rule
RT_TITLE  = "#262626"   # Cover page title text
RT_GREY   = "#7F7F7F"   # Footer text, secondary elements
RT_BODY   = "#000000"   # Main body text
RT_BORDER = "#C0C0C0"   # Table cell borders, HR
RT_LIGHT  = "#F2F2F2"   # Alternating table row background
```

### Replacing the logo

Drop a new `logo.svg` into the `assets/` directory. The generator looks for `assets/logo.svg` first,
then falls back to a plain text wordmark.

The logo is used in two places with different sizes:

- **Cover page** — `.cover-logo svg { height: 7mm; }` in the CSS block
- **Running header** — `.rt-hdr-right img { height: 10pt; }` in the CSS block

Adjust those values if your logo has a different aspect ratio.

### Changing page margins

In the `@page` rule inside the `CSS` block:

```css
@page {
    size: A4;
    margin: 28mm 20mm 28mm 20mm;  /* top right bottom left */
    ...
}
```

> **Important:** If you change the left/right margins, also update the explicit header width:
>
> ```css
> #rt-header {
>   width: 170mm;
> } /* = 210mm page − left margin − right margin */
> ```

### Changing the cover page layout

The cover HTML is in `HTML_TEMPLATE` between the `<div class="cover">` tags.
The cover CSS classes are in the `CSS` block under the `COVER PAGE` comment section.

### Adding new section types

The markdown parser in `md_to_html_body()` wraps every `##` heading in:

```html
<div class="section">
  <h2>...</h2>
  ...
</div>
```

The `.section` CSS class applies `page-break-before: always`. To suppress a page break
for a specific section, add a special case in the `if line.startswith("## "):` block and
use a different class without the page-break rule.

### Adding to the Document Control table

Pass extra metadata via `--scope` and `--subtitle`. To add completely custom rows,
edit the `extra_meta_rows` logic in `main()` and the corresponding `HTML_TEMPLATE`
table structure.

---

## Known Limitations

| Limitation                   | Notes                                                                                                                                                                        |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Images in markdown**       | Inline `![alt](path)` images are not rendered — embed base64 data URIs if needed                                                                                             |
| **Nested lists**             | Only single-level lists are supported                                                                                                                                        |
| **Footnotes / citations**    | Not supported                                                                                                                                                                |
| **Page number in HTML body** | CSS `counter(page)` only works in `@page` margin boxes, not in HTML elements                                                                                                 |
| **Footer rule gaps**         | Three `@bottom-*` margin boxes in WeasyPrint have hairline gaps at joins — the footer rule has been intentionally removed; use `border-top` on the boxes if you want it back |
| **Font embedding**           | WeasyPrint uses system fonts; Arial is used throughout. If Arial is unavailable, it falls back gracefully                                                                    |

---

## Changelog

| Version | Date       | Change                                                                                                                                                                                                                                                       |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | 2026-03-16 | Initial version — custom red/banner RT theme                                                                                                                                                                                                                 |
| 1.1     | 2026-03-16 | Rebuilt to authentic RT template (white cover, Arial, black h2 rule)                                                                                                                                                                                         |
| 1.2     | 2026-03-16 | SVG logo support, float header layout, grey footer, indented code fences fixed                                                                                                                                                                               |
| 1.3     | 2026-03-17 | Improved spacing throughout: h2 bottom gap 3pt→12pt, table cell padding 4pt→6pt, table margins 6pt→12pt top / 10pt→16pt bottom, h3/h4 bottom margins increased, list/HR spacing increased; `thead th` bottom border thickened to 1.5pt for visual separation |
| 1.4     | 2026-03-17 | TOC entries are now clickable PDF internal hyperlinks (anchor IDs slugified from heading text); large tables flow continuously across pages instead of being pushed to the next page; `thead` repeats on every continuation page                             |

---

_Maintained by Network Platform Team · Rio Tinto_
