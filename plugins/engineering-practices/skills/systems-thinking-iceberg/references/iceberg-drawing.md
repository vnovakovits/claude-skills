# Iceberg drawing template

The drawing this skill produces: a real iceberg, not a stack of boxes. Copy it, keep the shape and the
band boundaries, and replace the points inside each band with the findings for the problem at hand.

## Conventions

- **Waterline under Events.** Only Events sit above the water. Patterns sit just below it unless the
  organisation already charts them; say which in the caption.
- **Five bands, top to bottom:** Events, Patterns, Structures, Mental models, Vision. The ice darkens
  with depth (`--ice-top` → `--ice-4`) and the sea is a gradient (`--sea` → `--sea-deep`).
- **Points inside the ice.** Each band has a centred header (level name in mono caps, then the level's
  question in italics) and left-aligned bullet points. Lead a bullet with a bold key (`Board:`,
  `Espoused:`) when it names who holds the belief or which side of a comparison it is.
- **Margins carry the frame.** Kim's response mode for each level sits on the right, beside its band
  (React above the water, then Anticipate, Design, Reflect, Generate). A leverage arrow runs down the
  left from "Low leverage" to "High leverage".
- **Theme tokens only.** Every fill and text colour comes from a CSS token, so the drawing reads in light
  and dark. Define the tokens on `:root` with the usual dark-mode overrides (see `artifact-design`).

## Capacity per band (17px body text at the x shown)

| Band | y range | Bullet x | Lines | Max chars per line |
|---|---|---|---|---|
| Events (tip) | 56–230 | 396 | 4 | 30 |
| Patterns | 230–380 | 350 | 3 | 45 |
| Structures | 380–620 | 270 | 6 | 55 |
| Mental models | 620–850 | 250 | 6 | 55 |
| Vision | 850–1062 | 270 | 3 | 48 |

Lines are 22–24 units apart. If a band needs more, shorten the points: the drawing holds headlines,
and the detail goes in the findings beside it. Continuation lines indent by 16 units. Before
publishing, check that the start and end of every line sit inside the outline. Estimate width as
characters × 8.7 for body text and × 10.5 for headers, and test against the path's edges at the
line's y and y − 13. Keep at least 12 units clear of the outline.

## CSS

```css
.berg {
  --bw: min(1040px, calc(100vw - 32px));
  width: var(--bw);
  margin: 0 0 0 calc((100% - var(--bw)) / 2);
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--sea-deep);
}
.berg svg { display: block; width: 100%; min-width: 760px; height: auto; }
.berg .lvl { font: 600 18px var(--font-mono); letter-spacing: 0.1em; fill: var(--ice-fg); }
.berg .q { font: italic 400 17px var(--font-body); letter-spacing: 0; fill: var(--ice-fg); }
.berg .pt { font: 400 17px var(--font-body); fill: var(--ice-fg); }
.berg .pt tspan.k { font-weight: 600; }
.berg .mode-air { font: 500 16px var(--font-mono); fill: var(--muted); }
.berg .mode-sea { font: 500 16px var(--font-mono); fill: var(--sea-fg); }
.berg .wl { font: 500 13px var(--font-mono); letter-spacing: 0.1em; fill: var(--accent); }
```

The figure breaks out of a narrower reading column up to 1040px, and scrolls sideways inside its own
container below 760px so the text stays readable on a phone.

## SVG (worked example: incidents that cluster after releases)

```html
  <figure class="berg" aria-label="Iceberg model of recurring release incidents: only events show above the waterline; patterns, structures, mental models and vision sit below it, each with the findings for that level, and leverage rises with depth">
    <svg viewBox="0 0 1100 1100" xmlns="http://www.w3.org/2000/svg" role="img">
      <title>Systems-thinking iceberg: incidents after releases</title>
      <defs>
        <linearGradient id="seaGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" style="stop-color:var(--sea)"/>
          <stop offset="1" style="stop-color:var(--sea-deep)"/>
        </linearGradient>
        <clipPath id="bergClip">
          <path id="bergShape" transform="translate(20 0)" d="M300 230 L318 190 L350 150 L372 110 L410 78 L450 66 L500 56 L548 64 L600 76 L640 104 L672 140 L700 186 L740 230 L790 262 L840 310 L876 370 L900 440 L930 520 L950 610 L958 700 L944 790 L920 860 L880 930 L820 990 L720 1040 L600 1062 L470 1062 L350 1044 L250 1000 L180 940 L138 860 L114 770 L110 680 L124 590 L150 500 L184 420 L220 350 L262 280 Z"/>
        </clipPath>
      </defs>
      <rect x="0" y="0" width="1100" height="230" style="fill:var(--sky)"/>
      <rect x="0" y="230" width="1100" height="870" fill="url(#seaGrad)"/>
      <g clip-path="url(#bergClip)">
        <rect x="0" y="0" width="1100" height="230" style="fill:var(--ice-top)"/>
        <rect x="0" y="230" width="1100" height="150" style="fill:var(--ice-1)"/>
        <rect x="0" y="380" width="1100" height="240" style="fill:var(--ice-2)"/>
        <rect x="0" y="620" width="1100" height="230" style="fill:var(--ice-3)"/>
        <rect x="0" y="850" width="1100" height="250" style="fill:var(--ice-4)"/>
        <g style="stroke:var(--ice-fg);stroke-opacity:0.25;stroke-width:1.5;fill:none">
          <line x1="0" y1="380" x2="1100" y2="380"/>
          <line x1="0" y1="620" x2="1100" y2="620"/>
          <line x1="0" y1="850" x2="1100" y2="850"/>
        </g>
      </g>
      <use href="#bergShape" style="fill:none;stroke:var(--ice-fg);stroke-opacity:0.35;stroke-width:2"/>
      <line x1="0" y1="230" x2="1100" y2="230" style="stroke:var(--accent);stroke-width:2;stroke-dasharray:8 6"/>
      <text x="1086" y="220" text-anchor="end" class="wl">WATERLINE</text>

      <text x="540" y="110" text-anchor="middle" class="lvl">EVENTS</text>
      <text x="396" y="144" class="pt">• P1 after Thursday&#39;s release</text>
      <text x="396" y="166" class="pt">• Hotfix rolled back twice</text>
      <text x="396" y="188" class="pt">• Customer complaints spike</text>
      <text x="396" y="210" class="pt">• On-call paged at 02:00</text>
      <text x="540" y="270" text-anchor="middle" class="lvl">PATTERNS<tspan class="q" dx="10">· What keeps happening?</tspan></text>
      <text x="350" y="298" class="pt">• Incidents cluster after releases</text>
      <text x="350" y="322" class="pt">• Release batch size grows every month</text>
      <text x="350" y="346" class="pt">• Rollbacks up quarter on quarter</text>
      <text x="540" y="416" text-anchor="middle" class="lvl">STRUCTURES<tspan class="q" dx="10">· What causes the pattern?</tspan></text>
      <text x="270" y="444" class="pt">• A fortnightly release train batches changes</text>
      <text x="270" y="468" class="pt">• A change board approves every release</text>
      <text x="270" y="492" class="pt">• Integration tests run only before the release</text>
      <text x="270" y="516" class="pt">• No production metrics in the release review</text>
      <text x="270" y="540" class="pt">• On-call isn&#39;t the team that built the change</text>
      <text x="270" y="564" class="pt">• Fixes wait for the same train</text>
      <text x="540" y="658" text-anchor="middle" class="lvl">MENTAL MODELS<tspan class="q" dx="10">· What beliefs hold it in place?</tspan></text>
      <text x="250" y="686" class="pt">• <tspan class="k">Leadership:</tspan> more approval reduces risk</text>
      <text x="250" y="710" class="pt">• <tspan class="k">Leadership:</tspan> fewer releases mean fewer incidents</text>
      <text x="250" y="734" class="pt">• <tspan class="k">Developers:</tspan> testing is QA&#39;s job</text>
      <text x="250" y="758" class="pt">• <tspan class="k">Developers:</tspan> production is ops&#39; problem</text>
      <text x="250" y="782" class="pt">• <tspan class="k">Ops:</tspan> change is the enemy of stability</text>
      <text x="250" y="806" class="pt">• <tspan class="k">Everyone:</tspan> incidents are someone&#39;s mistake</text>
      <text x="540" y="888" text-anchor="middle" class="lvl">VISION<tspan class="q" dx="10">· What future is it serving?</tspan></text>
      <text x="270" y="916" class="pt">• <tspan class="k">Espoused:</tspan> fast, safe delivery to customers,</text>
      <text x="286" y="940" class="pt">learning from what we ship</text>
      <text x="270" y="964" class="pt">• <tspan class="k">In use:</tspan> no surprises at the change board</text>

      <text x="780" y="122" class="mode-air">What happened? · React</text>
      <text x="1000" y="312" class="mode-sea">Anticipate</text>
      <text x="1000" y="506" class="mode-sea">Design</text>
      <text x="1000" y="742" class="mode-sea">Reflect</text>
      <text x="1000" y="950" class="mode-sea">Generate</text>

      <text x="24" y="40" class="mode-air">Low leverage</text>
      <line x1="60" y1="56" x2="60" y2="230" style="stroke:var(--muted);stroke-width:2"/>
      <line x1="60" y1="230" x2="60" y2="1036" style="stroke:var(--sea-fg);stroke-width:2"/>
      <polygon points="52,1032 68,1032 60,1048" style="fill:var(--sea-fg)"/>
      <text x="24" y="1080" class="mode-sea">High leverage</text>
    </svg>
  </figure>
```
