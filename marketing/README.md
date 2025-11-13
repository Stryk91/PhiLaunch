# PhiVector Marketing Site

Static website for PhiVector ecosystem and PhiLaunch plugin.

## Structure

```
marketing/
├── index.html                          # PhiVector ecosystem homepage
├── plugins/
│   └── philaunch/
│       └── index.html                  # PhiLaunch plugin detail page
└── assets/
    ├── css/
    │   ├── phivector-colors.css        # Color system + Fibonacci spacing
    │   └── phivector-main.css          # Main stylesheet
    └── js/
        └── phivector-main.js           # Interactive features
```

## Design System

### Color Palette

**Industrial Tactical Multi-Color System**:
- Chrome/Metallic greys
- Neon cyan accents
- Fel green (tactical green)
- Blacks (lifted, not pure)
- Gunmetal grey
- Off-teal
- Pine (dark green)

### Mathematical Foundation

**Golden Ratio (φ = 1.618)** applied throughout:

**Fibonacci Spacing** (px):
```
3, 5, 8, 13, 21, 34, 55, 89, 144
```

**Fibonacci Timing** (ms):
```
89, 144, 233, 377, 610
```

**φ-based Easing**:
```css
cubic-bezier(0.618, 0, 0.382, 1)
```

**Typography** (Fibonacci px):
```
8, 13, 21, 34, 55, 89
```

**Grid System**:
- Golden ratio splits: 61.8% / 38.2%
- Fibonacci-based gaps

### Constraints

**Mandatory Rules**:
1. ALL spacing must use Fibonacci values (3/5/8/13/21/34/55/89px)
2. ALL font sizes must be Fibonacci (8/13/21/34/55/89px)
3. ALL animation durations must be Fibonacci milliseconds
4. ALL easing curves must use φ-based cubic-bezier
5. NO arbitrary values (10px, 15px, 20px are forbidden)

**Exceptions**:
- 1px borders (technical constraint)
- Percentages (for responsive grids)

## Brand Voice

**Style**: Industrial, tactical, angular, powerful, no-bullshit

**Tone**:
- Direct and concise
- Technical depth
- Zero marketing fluff
- Outcome-focused
- Mathematical precision

**What to Avoid**:
- Generic SaaS marketing speak
- Superlatives ("revolutionary", "amazing")
- Stock photo aesthetics
- Emoji (use sparingly, only in icons)
- Excessive enthusiasm

**What to Emphasize**:
- Mathematical foundations (φ, Fibonacci)
- Technical specifications
- Transparent security
- Local-first architecture
- Production-ready reliability

## Components

### Cards
```html
<div class="card">
    <h3 class="card-title">Title</h3>
    <p class="card-description">Description</p>
</div>
```

### Buttons
```html
<a href="#" class="btn btn-primary">Primary Action</a>
<a href="#" class="btn btn-secondary">Secondary Action</a>
<a href="#" class="btn btn-outline">Tertiary Action</a>
```

### Grids
```html
<!-- Equal columns -->
<div class="grid grid-2">...</div>
<div class="grid grid-3">...</div>

<!-- Golden ratio grid -->
<div class="grid-phi">...</div>
```

### Spacing Utilities
```html
<div class="p-13">Padding 13px (Fibonacci)</div>
<div class="m-21">Margin 21px (Fibonacci)</div>
<div class="gap-8">Gap 8px (Fibonacci)</div>
```

## JavaScript Features

- Smooth scroll for anchor links
- Fade-in animations on scroll
- Header shadow on scroll
- Stats counter animations (φ counter)
- Card hover glow effects
- Button ripple effects (φ-timed)
- Code block copy functionality
- Active nav link highlighting

All animations use φ-based timing (89/144/233/377/610ms).

## Responsive Breakpoints

```css
/* Desktop: 1440px+ (default) */

/* Tablet: 1024px */
@media (max-width: 1024px) {
    /* Grid adjustments */
}

/* Mobile: 768px */
@media (max-width: 768px) {
    /* Single column layouts */
}
```

## Browser Support

- Modern evergreen browsers (Chrome, Firefox, Safari, Edge)
- CSS Grid and Flexbox required
- JavaScript ES6+ features used
- No polyfills included (assume modern environment)

## Performance

- No external dependencies (besides Google Fonts)
- Pure HTML/CSS/JS (no frameworks)
- Minimal JavaScript
- Optimized for fast loading
- Static site (can deploy anywhere)

## Deployment

### GitHub Pages
```bash
# Enable GitHub Pages in repo settings
# Set source to /marketing directory
```

### Static Hosting
```bash
# Upload /marketing directory contents to:
# - Netlify
# - Vercel
# - CloudFlare Pages
# - Any static host
```

### Local Testing
```bash
# Python 3
cd marketing
python3 -m http.server 8080
# http://localhost:8080

# Or use dashboard server
cd ..
./start-dashboard.sh
# http://localhost:8080/marketing
```

## Customization

### Colors
Edit `assets/css/phivector-colors.css`:
```css
:root {
    --neon-cyan: #00F0FF;      /* Primary accent */
    --fel-green: #5FBF00;      /* Secondary accent */
    --gunmetal: #52595D;       /* Borders */
}
```

### Typography
Fonts are loaded from Google Fonts:
- **UI**: Inter
- **Mono**: JetBrains Mono
- **Display**: Rajdhani

To change fonts, update:
1. `<link>` tag in HTML
2. `--font-ui`, `--font-mono`, `--font-display` in CSS

### Timing
Adjust animation speeds in `phivector-colors.css`:
```css
:root {
    --timing-instant: 89ms;    /* Faster: 55ms */
    --timing-fast: 144ms;      /* Faster: 89ms */
    /* etc. (keep Fibonacci values) */
}
```

## Brand Assets Needed

**Logo**: Phi spiral (φ-based geometric spiral)
**Favicon**: Simplified phi symbol
**Icons**: Angular, industrial style
**Imagery**: No stock photos, technical diagrams preferred

## Content Guidelines

### Homepage
- Hero: Value proposition (1 sentence)
- Plugins: All ecosystem plugins listed
- Differentiators: What makes PhiVector unique
- Documentation: Link to guides
- Download: Full suite + individual plugins

### Plugin Pages
- Hero: Plugin-specific value prop
- Problem/Solution: What it solves
- Features: Specific capabilities (with code examples)
- Use Cases: Who it's for
- Architecture: Tech stack, structure
- Installation: Quick start guide
- Documentation: Links to guides
- Community: GitHub, issues, contributing

## SEO

**Title Pattern**:
```
PhiVector | [Value Proposition]
PhiLaunch | [Plugin Purpose]
```

**Meta Description**:
- 150-160 characters
- Keywords: mathematical, precision, automation, monitoring, etc.
- No fluff, direct description

**Keywords**:
- Golden ratio design
- Fibonacci architecture
- Remote automation
- Transparent security
- Local-first tools

## Accessibility

- WCAG 2.1 AA contrast ratios enforced
- Focus indicators on all interactive elements
- Semantic HTML structure
- `prefers-reduced-motion` support
- Keyboard navigation supported

## Version

**v1.0.0** - Initial marketing site
- PhiVector ecosystem homepage
- PhiLaunch plugin detail page
- Complete design system
- Interactive JavaScript features
- Full φ-based mathematical constraints

## License

Same as PhiLaunch repository.

---

**Built with mathematical precision. φ = 1.618**
