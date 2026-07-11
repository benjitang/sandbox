# js-sandbox

A JavaScript/TypeScript sandbox with two distinct parts living side by side:
a Next.js app for testing GSAP (or anything else that needs a browser/DOM),
and a folder of plain standalone Node scripts for quick syntax/logic tests
that don't need a UI at all.

## Requirements
- [Node.js](https://nodejs.org) (LTS version)
- `npm` (comes with Node)

## Project layout
```
js-sandbox/
├── src/
│   ├── app/             # Next.js routes — one folder per GSAP test/experiment
│   │   ├── page.tsx      # home page — links out to each test
│   │   └── tests/
│   │       ├── fade-in/
│   │       │   └── page.tsx
│   │       └── stagger/
│   │           └── page.tsx
│   ├── components/      # reusable React components shared across test pages
│   └── hooks/           # reusable custom hooks (e.g. useGsapTimeline)
├── scripts/              # standalone Node scripts — no browser, no React
│   ├── hello.js
│   └── array_methods_test.js
├── eslint.config.mjs
├── .prettierrc
└── package.json
```

## Part 1 — GSAP / browser tests (`src/`)

Anything that touches the DOM or needs to be *seen* goes here as a route.

### Running the dev server
```bash
npm run dev
```
Then open `http://localhost:3000` in the browser — the home page links out
to each test.

### Adding a new GSAP test
1. Create a new folder under `src/app/tests/`, e.g. `src/app/tests/scroll-trigger/`
2. Add a `page.tsx` inside it:
   ```tsx
   "use client";

   import { useEffect, useRef } from "react";
   import gsap from "gsap";

   export default function ScrollTriggerTest() {
     const boxRef = useRef<HTMLDivElement>(null);

     useEffect(() => {
       gsap.to(boxRef.current, { x: 200, duration: 1 });
     }, []);

     return <div ref={boxRef}>box</div>;
   }
   ```
3. Add a link to it on `src/app/page.tsx` so it shows up in the index.
4. Visit `http://localhost:3000/tests/scroll-trigger` — no restart needed,
   the dev server hot-reloads on save.

`"use client"` is required at the top of any file that uses hooks or
touches the DOM (GSAP falls into this category) — Next.js otherwise
assumes files are server-only.

### `components/` and `hooks/`
As tests accumulate, pull anything reused across more than one test page
out of the page file and into:
- **`src/components/`** — a UI piece (e.g. a reusable animated box) used by
  more than one test
- **`src/hooks/`** — repeated logic (e.g. a `useGsapTimeline` hook that sets
  up/cleans up a GSAP timeline) used by more than one test

If something's only used by one test page, leave it inline in that page —
no need to extract it just because a folder exists for it.

## Part 2 — plain script tests (`scripts/`)

Anything that's pure JavaScript logic — no DOM, no React, no browser —
goes here as a standalone file, run directly with Node.

### Running a script
```bash
node scripts/hello.js
```
Output prints straight to the terminal.

### Adding a new script
Just drop a new `.js`/`.ts` file into `scripts/` and run it with `node`.
No config, no build step, no restart of anything — it's a one-off file,
same as the individual `.cpp` files in the C++ sandbox.

```js
// scripts/hello.js
console.log("Hello world");
```

> Note: `.ts` files in `scripts/` need to be run through a TS runner (e.g.
> `npx tsx scripts/hello.ts`) since plain `node` doesn't execute
> TypeScript directly. For quick syntax tests, plain `.js` avoids that
> extra step; use `.ts` only when you specifically want to test typing.

## Formatting & linting
```bash
npx prettier --write .
npx eslint .
```
Both are configured project-wide (`.prettierrc`, `eslint.config.mjs`) and
apply to `src/` and `scripts/` alike.

## The rule of thumb
- **Testing something visual, animated, or DOM-related?** → new route
  under `src/app/tests/`
- **Testing plain JS/TS syntax, an algorithm, or a language feature with
  no UI?** → new file in `scripts/`, run with `node`