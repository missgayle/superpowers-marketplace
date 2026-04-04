# Activist Resiliency Website — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bilingual (EN/ES) static website for pro-democracy activists to access evidence-based resilience tools, grounded in the Working Framework for Moral Resiliency.

**Architecture:** Astro static site with markdown content pages, JSON resource data, and lightweight interactive components (self-check, resource filter, breathing guide). Content organized by locale (`/en/`, `/es/`). Deploys to Vercel from GitHub.

**Tech Stack:** Astro 5, vanilla CSS, minimal client-side JS, Vercel deployment

---

## File Structure

```
activist-resiliency/                   (project root — new directory in repo)
├── astro.config.mjs                   — Astro config with i18n and Vercel adapter
├── package.json                       — dependencies
├── tsconfig.json                      — TypeScript config
├── vercel.json                        — Vercel deployment config
├── public/
│   └── favicon.svg
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro           — shared HTML shell, nav, footer, lang switcher
│   ├── components/
│   │   ├── LanguageSwitcher.astro      — EN/ES toggle
│   │   ├── ResourceCard.astro          — single resource card display
│   │   ├── ResourceBrowser.astro       — filterable resource library (Read/Listen/Watch tabs)
│   │   ├── SelfCheck.astro             — crisis self-check routing component
│   │   └── BreathingGuide.astro        — CSS breathing animation
│   ├── pages/
│   │   ├── index.astro                 — landing page with two doorways
│   │   ├── en/
│   │   │   ├── crisis.astro            — acute crisis path
│   │   │   ├── resilience/
│   │   │   │   ├── index.astro         — resilience hub
│   │   │   │   ├── individuals.astro   — personal resilience
│   │   │   │   ├── organizers.astro    — team wellbeing
│   │   │   │   └── organizations.astro — structural resilience
│   │   │   ├── framework/
│   │   │   │   ├── index.astro         — moral resiliency model overview
│   │   │   │   ├── resilient-path.astro
│   │   │   │   └── reactive-path.astro
│   │   │   ├── resources.astro         — full resource library
│   │   │   └── science/
│   │   │       ├── index.astro         — science overview
│   │   │       ├── polyvagal.astro     — Porges
│   │   │       ├── window-of-tolerance.astro — Siegel
│   │   │       ├── climate-resilience.astro  — Epel
│   │   │       └── contemplative.astro — contemplative traditions
│   │   └── es/
│   │       └── (mirrors en/ structure)
│   ├── data/
│   │   └── resources.json              — all 30+ curated resources
│   ├── i18n/
│   │   ├── en.json                     — English UI strings
│   │   └── es.json                     — Spanish UI strings
│   └── styles/
│       └── global.css                  — design tokens, typography, layout system
```

---

## Task 1: Project Scaffolding

**Files:**
- Create: `activist-resiliency/package.json`
- Create: `activist-resiliency/astro.config.mjs`
- Create: `activist-resiliency/tsconfig.json`
- Create: `activist-resiliency/vercel.json`
- Create: `activist-resiliency/public/favicon.svg`

- [ ] **Step 1: Create project directory and initialize**

```bash
mkdir -p activist-resiliency
cd activist-resiliency
npm init -y
```

- [ ] **Step 2: Install Astro and Vercel adapter**

```bash
npm install astro @astrojs/vercel
```

- [ ] **Step 3: Create `astro.config.mjs`**

```javascript
import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel';

export default defineConfig({
  output: 'static',
  adapter: vercel(),
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es'],
    routing: {
      prefixDefaultLocale: true,
    },
  },
});
```

- [ ] **Step 4: Create `tsconfig.json`**

```json
{
  "extends": "astro/tsconfigs/strict"
}
```

- [ ] **Step 5: Create `vercel.json`**

```json
{
  "rewrites": [
    { "source": "/", "destination": "/en" }
  ]
}
```

- [ ] **Step 6: Create a minimal favicon**

Create `public/favicon.svg` — a simple green circle:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="14" fill="#7C9A6E"/>
</svg>
```

- [ ] **Step 7: Verify project builds**

```bash
cd activist-resiliency
npx astro build
```

Expected: Build succeeds (may warn about no pages yet).

- [ ] **Step 8: Commit**

```bash
git add activist-resiliency/
git commit -m "feat: scaffold Astro project with Vercel adapter and i18n config"
```

---

## Task 2: Global Styles and Design Tokens

**Files:**
- Create: `activist-resiliency/src/styles/global.css`

- [ ] **Step 1: Create global CSS with design tokens**

```css
:root {
  --color-sage: #7C9A6E;
  --color-sage-light: #A8BFA0;
  --color-clay: #C4836E;
  --color-clay-light: #D4A494;
  --color-cream: #FAF6F1;
  --color-gold: #C9A84C;
  --color-gold-light: #E0D5A0;
  --color-charcoal: #3A3632;
  --color-charcoal-light: #6B6560;
  --color-white: #FFFFFF;
  --font-body: 'Inter', 'Source Sans 3', system-ui, sans-serif;
  --font-heading: 'Lora', 'Literata', Georgia, serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1.125rem;
  --font-size-lg: 1.5rem;
  --font-size-xl: 2rem;
  --font-size-2xl: 2.75rem;
  --line-height-body: 1.7;
  --line-height-heading: 1.3;
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2.5rem;
  --space-xl: 4rem;
  --space-2xl: 6rem;
  --max-width: 72rem;
  --content-width: 48rem;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; }
body {
  font-family: var(--font-body);
  font-size: var(--font-size-base);
  line-height: var(--line-height-body);
  color: var(--color-charcoal);
  background-color: var(--color-cream);
}
h1, h2, h3, h4 { font-family: var(--font-heading); line-height: var(--line-height-heading); }
h1 { font-size: var(--font-size-2xl); }
h2 { font-size: var(--font-size-xl); }
h3 { font-size: var(--font-size-lg); }
a { color: var(--color-sage); }
a:hover { color: var(--color-clay); }
.container { max-width: var(--max-width); margin: 0 auto; padding: 0 var(--space-md); }
.content { max-width: var(--content-width); margin: 0 auto; }
```

- [ ] **Step 2: Commit**

```bash
git add activist-resiliency/src/styles/global.css
git commit -m "feat: add global CSS with earth-tone design tokens"
```

---

## Task 3: Base Layout and Navigation

**Files:**
- Create: `activist-resiliency/src/layouts/BaseLayout.astro`
- Create: `activist-resiliency/src/components/LanguageSwitcher.astro`
- Create: `activist-resiliency/src/i18n/en.json`
- Create: `activist-resiliency/src/i18n/es.json`

- [ ] **Step 1: Create EN and ES UI string files** (see spec for full content — nav labels, footer credits, language names)

- [ ] **Step 2: Create LanguageSwitcher component** — swaps `/en/` ↔ `/es/` in the current URL path

- [ ] **Step 3: Create BaseLayout** — HTML shell with Google Fonts (Inter + Lora), nav with links to all sections, "I Need Help Now" highlighted in clay color, footer with framework credit, language switcher

- [ ] **Step 4: Verify build**

```bash
cd activist-resiliency && npx astro build
```

- [ ] **Step 5: Commit**

```bash
git add activist-resiliency/src/layouts/ activist-resiliency/src/components/ activist-resiliency/src/i18n/
git commit -m "feat: add base layout with nav, footer, language switcher, and i18n"
```

---

## Task 4: Landing Page with Two Doorways

**Files:**
- Create: `activist-resiliency/src/pages/index.astro`
- Create: `activist-resiliency/src/pages/en/index.astro`
- Create: `activist-resiliency/src/pages/es/index.astro`

- [ ] **Step 1: Create root index that redirects to `/en`**

- [ ] **Step 2: Create EN landing page** — hero section ("You don't have to carry this alone."), two large clickable cards: "I Need Help Now" (clay gradient, links to `/en/crisis`) and "Build Resilience" (sage gradient, links to `/en/resilience`). Mobile-responsive single column.

- [ ] **Step 3: Create ES landing page** — same structure, Spanish text ("No tienes que cargar con esto solo/a.")

- [ ] **Step 4: Verify build**

- [ ] **Step 5: Commit**

```bash
git add activist-resiliency/src/pages/
git commit -m "feat: add landing page with two doorways in EN and ES"
```

---

## Task 5: Resource Data File

**Files:**
- Create: `activist-resiliency/src/data/resources.json`

- [ ] **Step 1: Create resources.json with all 30+ resources**

Each resource has: `id`, `title` (en/es), `description` (en/es), `format` (read/listen/watch), `type` (toolkit/guided-practice/educational/book/app/workbook), `stage` (acute/long-term/both), `audience` (individual/organizer/organization), `source`, `url`, `scienceTags`

Include all resources from the Vanina spreadsheet. Example entries:

```json
[
  {
    "id": "activist-handbook-wellbeing",
    "title": { "en": "Activist Handbook: Well-being", "es": "Manual del Activista: Bienestar" },
    "description": { "en": "This chapter offers mental health resources and strategies for activists.", "es": "Este capítulo ofrece recursos de salud mental y estrategias para activistas." },
    "format": "read",
    "type": "toolkit",
    "stage": ["both"],
    "audience": ["individual"],
    "source": "Activist Handbook",
    "url": "https://activisthandbook.org/wellbeing",
    "scienceTags": []
  },
  {
    "id": "levine-fight-flight",
    "title": { "en": "Fight or Flight Explanation", "es": "Explicación de Lucha o Huida" },
    "description": { "en": "Quick video of Peter Levine explaining the fight or flight response, and working with the freeze response.", "es": "Video corto de Peter Levine explicando la respuesta de lucha o huida, y trabajando con la respuesta de congelamiento." },
    "format": "watch",
    "type": "educational",
    "stage": ["acute"],
    "audience": ["individual"],
    "source": "Peter Levine",
    "url": "https://www.youtube.com/watch?v=GvM_6GOFDc4",
    "scienceTags": ["porges", "levine", "somatic"]
  }
]
```

Continue for all resources. Tag `scienceTags` based on relevance: `porges`, `levine`, `siegel`, `epel`, `somatic`, `contemplative`, `collective`.

- [ ] **Step 2: Commit**

```bash
git add activist-resiliency/src/data/resources.json
git commit -m "feat: add curated resource library data (30+ resources, EN/ES)"
```

---

## Task 6: Resource Card and Resource Browser Components

**Files:**
- Create: `activist-resiliency/src/components/ResourceCard.astro`
- Create: `activist-resiliency/src/components/ResourceBrowser.astro`

- [ ] **Step 1: Create ResourceCard** — displays one resource as a card with: format icon/badge (Read/Listen/Watch), title, description, source attribution, stage badge (Acute/Long-term), link to external URL. Card style uses earth-tone palette.

- [ ] **Step 2: Create ResourceBrowser** — three tabs (Read/Listen/Watch), filterable by stage (Acute/Long-term/All) and audience (Individual/Organizer/Organization/All). Uses client-side JS to filter the resource list. Falls back to showing all resources if JS disabled.

- [ ] **Step 3: Verify components render**

```bash
cd activist-resiliency && npx astro build
```

- [ ] **Step 4: Commit**

```bash
git add activist-resiliency/src/components/ResourceCard.astro activist-resiliency/src/components/ResourceBrowser.astro
git commit -m "feat: add ResourceCard and ResourceBrowser with filtering"
```

---

## Task 7: Resources Page

**Files:**
- Create: `activist-resiliency/src/pages/en/resources.astro`
- Create: `activist-resiliency/src/pages/es/resources.astro`

- [ ] **Step 1: Create EN resources page** — imports ResourceBrowser, passes all resources and lang='en'. Page title "Resources", intro text explaining the library.

- [ ] **Step 2: Create ES resources page** — same structure, Spanish text, lang='es'.

- [ ] **Step 3: Verify build**

- [ ] **Step 4: Commit**

```bash
git add activist-resiliency/src/pages/en/resources.astro activist-resiliency/src/pages/es/resources.astro
git commit -m "feat: add resources page with browsable library in EN and ES"
```

---

## Task 8: Breathing Guide Component

**Files:**
- Create: `activist-resiliency/src/components/BreathingGuide.astro`

- [ ] **Step 1: Create BreathingGuide** — CSS-only expanding/contracting circle animation. 4-second inhale, 4-second hold, 6-second exhale cycle. Text prompts change with each phase. Calm sage/cream colors. Centered on page. No JS required — pure CSS animation with `@keyframes`.

- [ ] **Step 2: Commit**

```bash
git add activist-resiliency/src/components/BreathingGuide.astro
git commit -m "feat: add CSS breathing guide animation component"
```

---

## Task 9: Self-Check Component

**Files:**
- Create: `activist-resiliency/src/components/SelfCheck.astro`

- [ ] **Step 1: Create SelfCheck** — 3 simple questions that route to different resources:
  - "What are you experiencing right now?" with options: "Overwhelmed / Racing thoughts" (hyper-arousal), "Numb / Shut down" (hypo-arousal), "I'm not sure"
  - Based on selection, shows a curated subset of acute resources appropriate to that state
  - "Overwhelmed" → grounding practices, breathing guide, calming meditations
  - "Numb" → gentle activation practices, yoga, body-awareness exercises
  - "Not sure" → shows breathing guide + general acute resources
  - Uses client-side JS for show/hide. Without JS, shows all acute resources.
  - Maps to the framework: overwhelmed = sympathetic activation / numb = dorsal vagal / breathing guide activates ventral vagal

- [ ] **Step 2: Commit**

```bash
git add activist-resiliency/src/components/SelfCheck.astro
git commit -m "feat: add self-check routing component for crisis page"
```

---

## Task 10: Crisis Page (Acute Path)

**Files:**
- Create: `activist-resiliency/src/pages/en/crisis.astro`
- Create: `activist-resiliency/src/pages/es/crisis.astro`

- [ ] **Step 1: Create EN crisis page** — immediately calming layout. Breathing guide at top. Self-check below. Contextual resources at bottom, prioritized by speed (watch > listen > read). Brief grounding text: "You are safe enough to be here. Let's start with a breath."

- [ ] **Step 2: Create ES crisis page** — same structure, Spanish text.

- [ ] **Step 3: Verify build and test navigation from landing page**

- [ ] **Step 4: Commit**

```bash
git add activist-resiliency/src/pages/en/crisis.astro activist-resiliency/src/pages/es/crisis.astro
git commit -m "feat: add crisis page with breathing guide and self-check"
```

---

## Task 11: Resilience Hub and Audience Pages

**Files:**
- Create: `activist-resiliency/src/pages/en/resilience/index.astro`
- Create: `activist-resiliency/src/pages/en/resilience/individuals.astro`
- Create: `activist-resiliency/src/pages/en/resilience/organizers.astro`
- Create: `activist-resiliency/src/pages/en/resilience/organizations.astro`
- Create: `activist-resiliency/src/pages/es/resilience/index.astro`
- Create: `activist-resiliency/src/pages/es/resilience/individuals.astro`
- Create: `activist-resiliency/src/pages/es/resilience/organizers.astro`
- Create: `activist-resiliency/src/pages/es/resilience/organizations.astro`

- [ ] **Step 1: Create EN resilience hub** — three pathway cards: Individuals (personal practices), Organizers (team wellbeing), Organizations (structural resilience). Each links to its subpage.

- [ ] **Step 2: Create EN individuals page** — content about personal resilience mapped to the Resilient Path: building perspective-taking, moral sensitivity, regulation practices. Links to relevant long-term resources filtered for individual audience.

- [ ] **Step 3: Create EN organizers page** — content about supporting team wellbeing: recognizing reactive path signs in team members, creating space for regulation, collective practices. Links to relevant resources.

- [ ] **Step 4: Create EN organizations page** — content about structural resilience: building cultures of coherence, invitational leadership, coalition building. Links to collective-tagged resources (Holistic Security manual, Protection International guides).

- [ ] **Step 5: Create ES versions** — translate all four pages to Spanish.

- [ ] **Step 6: Verify build**

- [ ] **Step 7: Commit**

```bash
git add activist-resiliency/src/pages/en/resilience/ activist-resiliency/src/pages/es/resilience/
git commit -m "feat: add resilience hub with individual, organizer, and organization pathways"
```

---

## Task 12: Framework Pages

**Files:**
- Create: `activist-resiliency/src/pages/en/framework/index.astro`
- Create: `activist-resiliency/src/pages/en/framework/resilient-path.astro`
- Create: `activist-resiliency/src/pages/en/framework/reactive-path.astro`
- Create: `activist-resiliency/src/pages/es/framework/index.astro`
- Create: `activist-resiliency/src/pages/es/framework/resilient-path.astro`
- Create: `activist-resiliency/src/pages/es/framework/reactive-path.astro`

- [ ] **Step 1: Create EN framework overview** — explains the Working Framework for Moral Resiliency. Visual diagram of the two paths (can be a styled HTML/CSS representation). Links to detailed pages for each path. Credits Gayle Karen Young, adapted from Eisenberg, Batson, Halifax, Rushton.

- [ ] **Step 2: Create EN resilient path page** — detailed explanation: Personal Attributes → Regulation & Integration → Other-Focused Behaviors → Personal/Inner outcomes (resilience, principled compassionate action, integrity, collective capability, discernment) + Collective/Outer outcomes (invitational leadership, collaboration, effective coalition building, coherence).

- [ ] **Step 3: Create EN reactive path page** — detailed explanation: Personal Attributes (low) → Dysregulation → Self-Focused Behaviors → Personal outcomes (burnout, unregulated action, acute secondary stress) + Collective outcomes (ineffective leadership, burning others out, silos, blaming).

- [ ] **Step 4: Create ES versions** of all three pages.

- [ ] **Step 5: Verify build**

- [ ] **Step 6: Commit**

```bash
git add activist-resiliency/src/pages/en/framework/ activist-resiliency/src/pages/es/framework/
git commit -m "feat: add framework pages explaining Moral Resiliency model"
```

---

## Task 13: Science Pages

**Files:**
- Create: `activist-resiliency/src/pages/en/science/index.astro`
- Create: `activist-resiliency/src/pages/en/science/polyvagal.astro`
- Create: `activist-resiliency/src/pages/en/science/window-of-tolerance.astro`
- Create: `activist-resiliency/src/pages/en/science/climate-resilience.astro`
- Create: `activist-resiliency/src/pages/en/science/contemplative.astro`
- Create: `activist-resiliency/src/pages/es/science/` (mirrors EN)

- [ ] **Step 1: Create EN science overview** — brief intro explaining the research grounding. Cards linking to each topic: Polyvagal Theory (Porges), Window of Tolerance (Siegel), Climate Resilience (Epel), Contemplative Traditions.

- [ ] **Step 2: Create EN polyvagal page** — explains polyvagal theory (ventral vagal = safety/social engagement, sympathetic = fight/flight, dorsal vagal = freeze/collapse). How it maps to the framework's regulation/dysregulation axis. Cross-references relevant resources (Levine video, Body Keeps the Score, trauma-sensitive yoga).

- [ ] **Step 3: Create EN window-of-tolerance page** — explains Siegel's concept (optimal arousal zone between hyper- and hypo-arousal). How activists move outside their window. Practices to widen it. Cross-references Siegel's Wheel of Awareness, guided meditations.

- [ ] **Step 4: Create EN climate-resilience page** — explains Epel's research on stress biology and sustained resilience. Application to long-haul activist work. Cross-references burnout workbooks, self-care assessments.

- [ ] **Step 5: Create EN contemplative page** — mindfulness, breathwork, embodied awareness. Lineage acknowledgment. Cross-references Kornfield meditation, Krishnananda meditations, IFS (Schwartz's No Bad Parts).

- [ ] **Step 6: Create ES versions** of all five pages.

- [ ] **Step 7: Verify build**

- [ ] **Step 8: Commit**

```bash
git add activist-resiliency/src/pages/en/science/ activist-resiliency/src/pages/es/science/
git commit -m "feat: add science pages — polyvagal, window of tolerance, climate resilience, contemplative"
```

---

## Task 14: Final Integration and Deployment

**Files:**
- Modify: `activist-resiliency/package.json` (add build/dev scripts)

- [ ] **Step 1: Ensure package.json has correct scripts**

```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  }
}
```

- [ ] **Step 2: Full build and test**

```bash
cd activist-resiliency && npm run build
```

Expected: Build succeeds with all pages generated.

- [ ] **Step 3: Test locally**

```bash
npm run preview
```

Verify: landing page loads, both doorways work, language switcher works, resources page filters work, crisis page breathing guide animates, all nav links resolve.

- [ ] **Step 4: Commit any final fixes**

```bash
git add -A activist-resiliency/
git commit -m "feat: final integration — all pages, components, and resources complete"
```

- [ ] **Step 5: Push to GitHub**

```bash
git push -u origin claude/install-superpowers-WGCkj
```

- [ ] **Step 6: Deploy to Vercel**

Connect the GitHub repo to Vercel. Set the root directory to `activist-resiliency/`. Framework preset: Astro. Deploy.

---

## Verification

After deployment, verify end-to-end:

1. Landing page loads at root URL, redirects to `/en`
2. "I Need Help Now" leads to crisis page with breathing guide and self-check
3. "Build Resilience" leads to resilience hub with three audience pathways
4. Resource library shows all 30+ resources, filterable by Read/Listen/Watch, stage, audience
5. Framework pages display the Moral Resiliency model with both paths
6. Science pages explain each research foundation with cross-referenced resources
7. Language switcher toggles all pages between EN and ES
8. Site loads fast on mobile
9. All external resource links open correctly
