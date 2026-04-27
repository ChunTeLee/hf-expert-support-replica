<!--
  Hugging Face Expert Support — replica wrapped as a SvelteKit page component.

  Drop this file into a SvelteKit route (e.g. src/routes/+page.svelte) and
  copy the asset folders (figma/, *.svg, *.png, style.css, bars.css) into
  the project's `static/assets/` directory. Asset paths below assume
  /assets/... resolves from the web root (the SvelteKit static convention).
  If you're using plain Svelte without SvelteKit, change the absolute /assets
  paths to whatever path your bundler exposes the static files under.

  Theme defaults to dark (the folder name is "dark"); the sun/moon button
  in the top-right toggles, with the choice persisted to localStorage and
  honoured on the next reload.
-->

<script>
  import { onMount } from 'svelte';

  let isDark = true;

  // Inline every .bars-layer <img> as inline <svg> so the var(--fill-0),
  // var(--stroke-0), var(--top-fill) references inside the SVGs actually
  // resolve from the page's CSS variables. Without inlining, <img src>
  // SVGs don't see parent CSS vars and the dark-theme overrides have no
  // effect on the bar paths.
  async function inlineBars() {
    const imgs = Array.from(document.querySelectorAll('.bars-layer img'));
    const cache = new Map();
    await Promise.all(imgs.map(async (img) => {
      const src = img.getAttribute('src');
      let p = cache.get(src);
      if (!p) {
        p = fetch(src).then((r) => r.text());
        cache.set(src, p);
      }
      const text = await p;
      const doc = new DOMParser().parseFromString(text, 'image/svg+xml');
      const svg = doc.documentElement;

      svg.querySelectorAll('stop[stop-color="white"]').forEach((stop) => {
        stop.setAttribute('stop-color', 'var(--fill-0, white)');
      });
      svg.querySelectorAll('path[fill="#FBFCFC"]').forEach((path) => {
        path.setAttribute('fill', 'var(--top-fill, #FBFCFC)');
      });

      svg.setAttribute('width', '100%');
      svg.setAttribute('height', '100%');
      svg.style.display = 'block';
      img.replaceWith(svg);
    }));
  }

  function applyTheme(dark) {
    document.documentElement.classList.toggle('dark', dark);
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (_) {}
  }

  function toggleTheme() {
    isDark = !isDark;
    applyTheme(isDark);
  }

  onMount(() => {
    // Resolve the persisted theme. Falls back to OS preference, then
    // finally to dark (this is the "dark" export, after all).
    let stored = null;
    try { stored = localStorage.getItem('theme'); } catch (_) {}
    const systemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    isDark = stored ? stored === 'dark' : (systemDark ? true : true);
    applyTheme(isDark);
    inlineBars();
  });
</script>

<svelte:head>
  <title>Expert Support – Hugging Face</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;1,200;1,300;1,400;1,600;1,700&display=swap" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&display=swap" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" />
  <link rel="stylesheet" href="/assets/style.css" />
  <link rel="stylesheet" href="/assets/bars.css" />
  <!--
    NOTE: Synchronous theme bootstrap (light/dark resolution before paint)
    cannot live here — scripts injected via {@html} in <svelte:head> are
    not executed by the browser. Paste the snippet from README.md into
    your project's `app.html` instead so it runs before hydration. Without
    that snippet, first paint will briefly use the default theme and then
    flip to the persisted choice once `onMount` runs below.
  -->
</svelte:head>

<div class="flex min-h-dvh flex-col bg-white dark:bg-gray-950">
  <header class="border-b border-gray-100 dark:border-gray-850 ">
    <div class="w-full px-4 container flex h-16 items-center">
      <div class="flex flex-1 items-center">
        <a class="mr-5 flex flex-none items-center lg:mr-6" href="/">
          <img alt="Hugging Face's logo" class="w-7 md:mr-2" src="/assets/huggingface_logo-noborder.svg" />
          <span class="hidden whitespace-nowrap text-lg font-bold md:block">Hugging Face</span>
        </a>
        <div class="relative flex-1 lg:max-w-sm mr-2 sm:mr-4 md:mr-3 xl:mr-6">
          <input autocomplete="off" spellcheck="false" type="text"
                 class="w-full dark:bg-gray-950 pl-8 form-input-alt h-9 pr-3 focus:shadow-xl"
                 name="" placeholder="Search models, datasets, users..." />
          <svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" role="img"
               width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"
               class="absolute left-2.5 text-gray-400 top-1/2 transform -translate-y-1/2">
            <path d="M30 28.59L22.45 21A11 11 0 1 0 21 22.45L28.59 30zM5 14a9 9 0 1 1 9 9a9 9 0 0 1-9-9z" fill="currentColor"></path>
          </svg>
        </div>
        <div class="flex flex-none items-center justify-center p-0.5 place-self-stretch lg:hidden">
          <button class="relative z-40 flex h-6 w-8 items-center justify-center" type="button">
            <svg width="1em" height="1em" viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" role="img" preserveAspectRatio="xMidYMid meet" fill="currentColor" class="text-xl">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M1.65039 2.9999C1.65039 2.8066 1.80709 2.6499 2.00039 2.6499H8.00039C8.19369 2.6499 8.35039 2.8066 8.35039 2.9999C8.35039 3.1932 8.19369 3.3499 8.00039 3.3499H2.00039C1.80709 3.3499 1.65039 3.1932 1.65039 2.9999ZM1.65039 4.9999C1.65039 4.8066 1.80709 4.6499 2.00039 4.6499H8.00039C8.19369 4.6499 8.35039 4.8066 8.35039 4.9999C8.35039 5.1932 8.19369 5.3499 8.00039 5.3499H2.00039C1.80709 5.3499 1.65039 5.1932 1.65039 4.9999ZM2.00039 6.6499C1.80709 6.6499 1.65039 6.8066 1.65039 6.9999C1.65039 7.1932 1.80709 7.3499 2.00039 7.3499H8.00039C8.19369 7.3499 8.35039 7.1932 8.35039 6.9999C8.35039 6.8066 8.19369 6.6499 8.00039 6.6499H2.00039Z"></path>
            </svg>
          </button>
        </div>
      </div>
      <nav aria-label="Main" class="ml-auto hidden lg:block">
        <ul class="flex items-center gap-x-1 2xl:gap-x-2">
          <li class="hover:text-indigo-700"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/models">Models</a></li>
          <li class="hover:text-red-700"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/datasets">Datasets</a></li>
          <li class="hover:text-blue-700"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/spaces">Spaces</a></li>
          <li class="hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 max-xl:hidden"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/storage">Buckets <span class="ml-1.5 translate-y-px rounded bg-blue-600/15 px-1 py-px text-[.65rem] font-bold uppercase leading-tight text-blue-600 dark:bg-blue-500/20 dark:text-blue-300">new</span></a></li>
          <li class="hover:text-yellow-700"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/docs">Docs</a></li>
          <li class="hover:text-black dark:hover:text-white max-2xl:hidden"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/enterprise">Enterprise</a></li>
          <li><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/pricing">Pricing</a></li>
          <li><hr class="h-5 w-0.5 border-none bg-gray-100 dark:bg-gray-800" /></li>
          <li><a class="block cursor-pointer whitespace-nowrap px-2 py-0.5 hover:text-gray-500 dark:text-gray-300 dark:hover:text-gray-100" href="/login">Log In</a></li>
          <li><a class="whitespace-nowrap rounded-full border border-transparent bg-gray-900 px-3 py-1 leading-none text-white hover:border-black hover:bg-white hover:text-black" href="/join">Sign Up</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main class="flex flex-1 flex-col">
    <div class="relative min-h-screen overflow-clip bg-white dark:bg-gray-950">
      <div class="border-b border-gray-200/70 px-4">
        <section class="relative z-1 mx-auto flex max-w-7xl flex-col items-center overflow-hidden text-balance border-x border-gray-200/70 px-4 pb-0 pt-8 sm:px-6 sm:pt-12 lg:px-8">
          <div class="relative px-2 py-12 text-center sm:px-12 sm:py-16 lg:px-16 lg:py-20">
            <h1 class="relative mb-4 text-pretty text-5xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl md:text-7xl">
              Hugging Face <span class="relative inline-block"><span class="bg-linear-to-b relative from-black from-45% to-gray-400 bg-clip-text font-bold text-transparent dark:from-white dark:to-gray-400">Expert Support</span></span>
            </h1>
            <p class="relative mb-6 text-2xl text-gray-600 dark:text-gray-400 xl:mb-12">Unlock the impact of Hugging Face faster, with us</p>
            <div class="flex flex-col items-center gap-3">
              <a href="/contact/sales?from=support" class="whitespace-nowrap rounded-full bg-black px-6 py-1.5 text-lg text-white ring-1 ring-gray-300 ring-offset-4 transition-all hover:ring-black dark:bg-gray-300 dark:text-black dark:ring-gray-300 dark:ring-offset-gray-950">
                <span class="mr-0.5">→</span> Talk to Sales
              </a>
              <p class="text-smd max-w-[200px] text-balance text-gray-500">to discuss your project and requirements</p>
            </div>
          </div>

          <div class="iso-stage" aria-hidden="true">
            <div class="iso-grid-bg-cover"></div>
            <div class="iso-grid-bg"></div>
            <div class="bars-layer">
              <span class="bar bar-2685 bar-left"><img src="/assets/figma/v1.svg" alt="" /></span>
              <span class="bar bar-2687 flip bar-right"><img src="/assets/figma/v3.svg" alt="" /></span>
              <span class="bar bar-2688 bar-right"><img src="/assets/figma/v4.svg" alt="" /></span>
              <span class="bar bar-2689 flip bar-right"><img src="/assets/figma/v5.svg" alt="" /></span>
              <span class="bar bar-2690 flip bar-right"><img src="/assets/figma/v6.svg" alt="" /></span>
              <span class="bar bar-2691 bar-right"><img src="/assets/figma/v7.svg" alt="" /></span>
              <span class="bar bar-2692 flip bar-right"><img src="/assets/figma/v8.svg" alt="" /></span>
              <span class="bar bar-2693 bar-right"><img src="/assets/figma/v9.svg" alt="" /></span>
              <span class="bar bar-2694 flip bar-right"><img src="/assets/figma/v10.svg" alt="" /></span>
              <span class="bar bar-2695 bar-left"><img src="/assets/figma/v11.svg" alt="" /></span>
              <span class="bar bar-2696 flip bar-left"><img src="/assets/figma/v12.svg" alt="" /></span>
              <span class="bar bar-2697 bar-left"><img src="/assets/figma/v13.svg" alt="" /></span>
              <span class="bar bar-2698 flip bar-left"><img src="/assets/figma/v14.svg" alt="" /></span>
              <span class="bar bar-2699 bar-left"><img src="/assets/figma/v15.svg" alt="" /></span>
              <span class="bar bar-2700 flip bar-left"><img src="/assets/figma/v16.svg" alt="" /></span>
              <span class="bar bar-2701 flip bar-left"><img src="/assets/figma/v17.svg" alt="" /></span>
              <span class="bar bar-2702 flip bar-left"><img src="/assets/figma/v18.svg" alt="" /></span>
              <span class="bar bar-2703 bar-right"><img src="/assets/figma/v19.svg" alt="" /></span>
              <span class="bar bar-2704 bar-right"><img src="/assets/figma/v19.svg" alt="" /></span>
              <span class="bar bar-2705 bar-right"><img src="/assets/figma/v19.svg" alt="" /></span>
              <span class="bar bar-2706 bar-right"><img src="/assets/figma/v19.svg" alt="" /></span>
              <span class="bar bar-2686 bar-right"><img src="/assets/figma/v2.svg" alt="" /></span>
              <span class="bar bar-2707 bar-right"><img src="/assets/figma/v20.svg" alt="" /></span>
              <span class="bar bar-2708 bar-left"><img src="/assets/figma/v21.svg" alt="" /></span>
              <span class="bar bar-2709 bar-left"><img src="/assets/figma/v22.svg" alt="" /></span>
              <span class="bar bar-2710 bar-left"><img src="/assets/figma/v23.svg" alt="" /></span>
              <span class="bar bar-2711 bar-left"><img src="/assets/figma/v23.svg" alt="" /></span>
              <span class="bar bar-2712 bar-left"><img src="/assets/figma/v24.svg" alt="" /></span>
            </div>
          </div>
        </section>

        <section class="relative z-5 w-full bg-white dark:bg-gray-950">
          <div class="relative z-1 mx-auto flex w-full max-w-7xl items-center justify-center border-x border-t border-gray-200/70 px-6 py-3 text-center dark:border-gray-850 md:px-10 md:py-5">
            <p class="text-balance text-gray-500">
              Unlock priority support for Hugging Face and
              <span class="text-black dark:text-white">build better AI in-house</span>
              with Hugging Face Experts.
            </p>
          </div>
        </section>
      </div>

      <section class="relative z-5 w-full border-b border-gray-200/70 px-4">
        <div class="relative mx-auto h-16 max-w-7xl border-x border-gray-200/70"></div>
      </section>
    </div>
  </main>
</div>

<button id="theme-toggle" type="button" aria-label="Toggle theme"
  on:click={toggleTheme}
  class="fixed right-4 top-20 z-50 flex h-9 w-9 items-center justify-center rounded-full border border-gray-200 bg-white/95 text-gray-700 shadow-sm backdrop-blur-sm transition-colors hover:border-gray-400 dark:border-gray-700 dark:bg-gray-900/95 dark:text-gray-200 dark:hover:border-gray-500">
  <svg class="theme-icon-sun h-4 w-4 dark:hidden" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
  </svg>
  <svg class="theme-icon-moon hidden h-4 w-4 dark:block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
  </svg>
</button>
