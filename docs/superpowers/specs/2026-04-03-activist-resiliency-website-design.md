# Activist Resiliency Website — Design Spec

## Purpose

A bilingual (English/Spanish) website for international pro-democracy activists, organizers, and organizations to access evidence-based resilience tools grounded in polyvagal theory, somatic psychology, and contemplative traditions. The site is structured around the Working Framework for Moral Resiliency (Gayle Karen Young, adapted from Eisenberg, Batson, Halifax, Rushton).

## Framework Engine: Moral Resiliency Model

The site's architecture maps directly to the dual-path model:

**Resilient Path** (Inhabited, Responsive/Collective):
- Personal Attributes (high perspective-taking, moral sensitivity, resourced, capacity for complexity) + Regulation & Integration (practices, ritual, community, creative acts) → Other-focused behaviors (empathy-related responses, generative sensemaking, moral imagination) → Personal resilience + Collective coherence (invitational leadership, collaboration, coalition building)

**Reactive Path** (Habituated/Isolated):
- Personal Attributes (low perspective-taking, under-resourced, complexity-avoidant) + Dysregulation (empathic distress, over-arousal) → Self-focused behaviors (avoidance, numbness, isolation, unregulated moral outrage) → Burnout + Ineffective leadership (silos, blaming, burning others out)

The site helps users recognize which path they're on and move from reactive to resilient, with different interventions for acute crisis vs. chronic depletion.

## Audiences

Three distinct pathways:

1. **Individual activists** — personal resilience tools (self-regulation, recovery, somatic practices)
2. **Movement organizers/leaders** — supporting team wellbeing at scale
3. **International pro-democracy organizations/NGOs** — building resilience into operational structure

## Site Architecture

```
/ (landing page)
├── Two doorways: "I Need Help Now" / "Build Resilience"
│
├── /crisis (acute path)
│   ├── "What are you experiencing?" — simple self-check
│   ├── Matched practices (breathing, grounding, somatic)
│   └── Contextual resources from library
│
├── /resilience (long-term path)
│   ├── /individuals — personal resilience practices
│   ├── /organizers — supporting team wellbeing
│   └── /organizations — structural resilience
│
├── /framework — Moral Resiliency model explained
│   ├── Resilient Path
│   └── Reactive Path
│
├── /resources — Full resource library
│   ├── Filtered by: Read / Listen / Watch
│   ├── Filtered by: Acute / Long-term
│   └── Filtered by: Audience / Language
│
└── /science — Research grounding
    ├── Porges (polyvagal theory)
    ├── Siegel (window of tolerance)
    ├── Epel (climate resilience)
    ├── Levine (somatic experiencing)
    └── Contemplative traditions
```

All pages available in `/en/` and `/es/`.

## Content & Data Model

### Resources (JSON)

All resources from the curated library stored in `content/data/resources.json`:

```json
{
  "id": "levine-fight-flight",
  "title": { "en": "Peter Levine: Fight or Flight Explanation", "es": "..." },
  "description": { "en": "Quick video explaining the fight or flight response...", "es": "..." },
  "format": "watch",
  "type": "educational",
  "stage": ["acute"],
  "audience": ["individual"],
  "source": "Peter Levine",
  "url": "https://www.youtube.com/watch?v=GvM_6GOFDc4",
  "scienceTags": ["porges", "levine", "somatic"]
}
```

Format values: `read` (PDFs, articles, workbooks, books), `listen` (Spotify, podcasts, apps), `watch` (YouTube, video)

Type values: `toolkit`, `guided-practice`, `educational`, `book`, `app`, `workbook`

Stage values: `acute`, `long-term`, `both`

Audience values: `individual`, `organizer`, `organization`

### Framework Content (Markdown)

```
content/
├── en/
│   ├── crisis/          — acute path pages
│   ├── resilience/      — long-term path (individuals, organizers, orgs)
│   ├── framework/       — Resilient Path, Reactive Path
│   └── science/         — Porges, Siegel, Epel, contemplative traditions
├── es/
│   └── (same structure, translated)
└── data/
    └── resources.json
```

### Resource Integration

Resources appear in three contexts:

1. **`/resources`** — full browsable library with Read/Listen/Watch tabs and filtering
2. **`/science`** — cross-referenced on relevant science pages (e.g., Levine video appears on the Porges/polyvagal page)
3. **Crisis/resilience pathways** — surfaced contextually based on stage and audience

Science page cross-references:
- **Porges/Levine** → Levine fight-or-flight video, Waking the Tiger, trauma-sensitive yoga, Body Keeps the Score
- **Siegel** → Wheel of Awareness, guided presence meditations
- **Somatic/body-based** → yoga sessions, Breathwrk app, Levine's somatic work
- **Epel/sustained resilience** → burnout workbooks, self-care assessments, Amnesty sustainable activism guides
- **Contemplative traditions** → Kornfield meditation, Krishnananda meditations, IFS (Schwartz)
- **Collective/structural** → Holistic Security manual, Protection International guides

Reading list (van der Kolk, Levine, Wolynn, Schwartz) appears in `/resources` under Read and in `/science` as recommended deeper learning.

## Self-Check Component

A simple 3-5 question interactive element on the crisis page. Not a clinical assessment — routing only.

Maps to the framework's dysregulation indicators:
- "Are you feeling activated/overwhelmed right now?" → surfaces grounding practices (ventral vagal activation)
- "Are you feeling numb/depleted?" → surfaces gentle activation practices
- Routes to appropriate resources by format preference

## Visual Design

**Palette:** Warm earth tones — soft sage greens, warm clay/terracotta, cream/off-white backgrounds, muted gold accents. Dark text in warm charcoal (not pure black).

**Typography:** Humanist sans-serif (Inter or Source Sans) for body. Gentle serif (Lora or Literata) for headings.

**Layout principles:**
- Generous whitespace — spacious, not crowded
- Large readable text — activists may read under stress
- Minimal visual noise — no stock photos, no busy patterns
- Subtle illustrations/icons for navigation
- Simple breath animation on crisis page (CSS expanding/contracting circle)
- Mobile-first — many users on phones, possibly under duress

**Crisis doorway:** Immediately calming. No extra clicks before a practice. Breathing exercise on the page. Resources prioritized by speed (watch 3-min video > read workbook).

**Resilience doorway:** Structured, exploratory. Audience pathway selection. Progressive depth.

**Resource library:** Three-tab layout (Read/Listen/Watch). Filterable sidebar (stage, audience, language). Card-based entries with source attribution.

## Technical Stack

- **Astro** — static site generator with component islands
- **Astro i18n routing** — `/en/` and `/es/` prefixes, language switcher in header
- **Vanilla CSS** (Astro scoped styles) — no UI framework
- **Deployment:** Vercel (primary), portable to GitHub Pages or Netlify
- **Content portable to Squarespace** via embeddable widgets for interactive components

### Interactive Components (Astro islands, minimal JS):
- Self-check router — show/hide content based on selections
- Resource browser — client-side filtering by format/stage/audience/language
- Breathing guide — CSS animation with timed text
- Language switcher — toggles between locale equivalents

### Not Building:
- No user accounts or login
- No database — static JSON + markdown
- No server-side logic
- No analytics (can add Plausible later)
- No comment system or social features

### Performance:
- Static HTML for near-instant load times globally
- Critical for activists on VPNs, slow connections, or restrictive networks
- Entire site works without JavaScript (except self-check and resource filtering)

## Science & Editorial Stance

Science-led with contemplative traditions given real presence — not subordinate, not just footnotes.

Research foundations:
- **Stephen Porges** — polyvagal theory (ventral vagal = social engagement/safety, sympathetic = fight/flight, dorsal vagal = freeze/collapse)
- **Dan Siegel** — window of tolerance (optimal arousal zone between hyper- and hypo-arousal)
- **Elissa Epel** — climate resilience research, stress biology, telomere science applied to sustained activist work
- **Peter Levine** — somatic experiencing, completing the stress response cycle
- **Contemplative traditions** — mindfulness, breathwork, embodied awareness practices with lineage acknowledgment

## Curated Resource Library

30+ resources from the Vanina Mental Health collection, tagged and categorized:

### Watch (Video)
- Yoga Healing Body and Soul (Yoga with Adriene)
- Guided sleep meditation for trauma-based insomnia (The Mindful Movement)
- Guided Meditation on Being Present (Jack Kornfield)
- Understanding and Exploring Awareness / Wheel of Awareness (Dan Siegel)
- Short Yoga Flow for Exhaustion and Burnout (Honey Lion)
- Evidence-based trauma-sensitive yoga (Trauma Center)
- Peter Levine fight or flight explanation (Peter Levine)

### Listen (Audio/Apps)
- Guided Meditation for Fear (Krishnananda and Amana)
- Guided Meditation to Grow Inner Space (Krishnananda and Amana)
- Breathwrk App

### Read (Articles/PDFs/Workbooks/Books)
- Activist Handbook: Well-being chapter
- Police Brutality & Activist Trauma Support and Recovery (Roots of Change Collective)
- Protecting Your Mental Health While Speaking Out (Malala Fund)
- Holistic Security: A Strategy Manual for Human Rights Defenders (Tactical Tech)
- Self-Care for Activists (Augsburg University)
- 21-Day Activism Self-Care Challenge (Debby Irving et al.)
- Self-care and burnout prevention toolkit (Frontline Aids)
- Staying Resilient While Trying to Save the World Vol 1 & 2 (Amnesty International)
- Manual to Prevent Criminalisation of Defenders (Protection International) — Spanish
- Taking Care of Us: Collective Protection Guide (Protection International)
- Burnout Workbook (Support Link)
- Healing Trauma Worksheets (Positive Psychology)
- Self Care Assessment and Plan Builder (Brown University)
- Resources for Finding Affordable Trauma Therapy (Free Psychotherapy Network)
- Understanding Your Panic Attack (Better Health Channel)
- Understanding Your Anxiety (McLean Hospital)
- Sustainable Activism and Self-Care (Amnesty International)
- The Body Keeps the Score (Bessel van der Kolk)
- Waking the Tiger (Peter Levine)
- It Didn't Start With You (Mark Wolynn)
- No Bad Parts (Richard Schwartz)
