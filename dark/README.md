# dark/ — Svelte export of the Expert Support replica

`+page.svelte` is the full hero + nav wrapped as a SvelteKit page component.
Dark theme is the default; the sun/moon button in the top-right toggles to
light, and the choice is persisted to `localStorage` so it survives reloads.

## Drop-in steps (SvelteKit)

1. Copy `+page.svelte` into your route, e.g. `src/routes/+page.svelte`.
2. Copy these from this repo's `replica/assets/` into your project's
   `static/assets/` so the `/assets/...` paths resolve:
   - `style.css`, `bars.css`
   - `figma/` (the bar SVGs — `v1.svg` … `v24.svg`)
   - `iso-grid-tile.svg`, `iso-grid-tile-dark.svg`
   - `huggingface_logo-noborder.svg`
3. (Optional, recommended) Move the synchronous theme bootstrap script
   from `<svelte:head>` into your shell's `app.html` so it runs before
   the first paint instead of after hydration. The block to copy is the
   `{@html '<script>...</script>'}` line — its body sets
   `document.documentElement.classList` based on `localStorage.theme`
   or `prefers-color-scheme`.

## Drop-in steps (plain Svelte)

Same as above, but rewrite the absolute `/assets/...` paths to whatever
relative path your bundler exposes the static files under. If you use
Vite, putting the assets in `public/assets/` keeps the existing paths
working unchanged.

## What's in the script

- `inlineBars()` — fetches every `.bars-layer img` SVG, parses it, rewires
  hard-coded `stop-color="white"` and `fill="#FBFCFC"` to `var(--fill-0)`
  and `var(--top-fill)` so the dark-theme overrides on `.iso-stage` reach
  into the inlined paths, then replaces the `<img>` with the inline SVG.
- `applyTheme(dark)` — flips `html.dark`, sets `data-theme`, writes to
  `localStorage`.
- `onMount` — reads `localStorage` (else `prefers-color-scheme`, else
  defaults to dark since this is the dark export), calls `applyTheme`,
  and runs the inline pass once.
