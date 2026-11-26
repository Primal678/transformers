# Synthetic Cinema

A browsable archive of AI-generated movies, series, music videos and ads, from *Sunspring* (2016) to current Sora, Veo and Runway productions.

## Run it

It's a single static page with no build step. Open `index.html` in a browser, or serve the folder:

```bash
cd ai-movies-app && python3 -m http.server 8000   # then visit http://localhost:8000
```

## Features

- Search by title, creator or AI tool; filter by format (short, feature, series, music video, commercial, AI-assisted) and by tool; sort by year or title.
- Detail view for each title with creator, runtime, tools, and where it streams, plus "Find on YouTube" and web-search links so you always land on the current upload.
- **Find new uploads**: live feeds and searches (YouTube, r/aivideo, Runway AI Film Festival, Sora, Showrunner, Vimeo, Curious Refuge) where new AI films appear daily.
- **Add a title**: add anything you find; it's saved in your browser's localStorage.

## Editing the catalog

Titles live in the `CATALOG` array in `index.html` (`app.html` is the same page without the `<html>/<head>` wrapper, used for the hosted Artifact version). Each entry:

```js
{ t: "Title", y: 2025, type: "Short film", by: "Creator", tools: ["Sora"], rt: 4, where: "YouTube", d: "Description" }
```

`rt` is runtime in minutes (`0` for episodic). Add `status: "Announced"` for unreleased titles.
