# Extended Car Warranty Hub

This is a high-performance, statically generated website optimized for Google Search and Google AdSense.

## Architecture
- All content is written in Markdown within `_src/content/`.
- The site is built into raw static HTML, CSS, and JS directly into the repository root using the Python generator.
- This root-level deployment is necessary for cPanel's Git™ Version Control system to serve the static files directly.

## Deployment
Every `git push` will trigger the cPanel deployment via the included `.cpanel.yml` file.

## How to Add New Articles
1. Create a new markdown file in `_src/content/articles/` (e.g. `my-new-guide.md`).
2. Add the required frontmatter:
```yaml
---
title: "Your Title Here"
description: "Your SEO meta description here"
author: "Fleet Protection Expert"
date: "2024-05-01"
slug: "your-title-here"
---
```
3. Write your markdown content below the frontmatter.
4. Run `python _src/build_site.py` from the root directory to compile the new HTML file.
5. Commit and push the changes.

## Adding AdSense
The ad placeholders are located in `_src/templates/article.html` and `_src/templates/index.html`. You can replace the placeholder text with your actual AdSense `<ins>` blocks, then run the build script.

## Connect Newsletter
The newsletter form is in `_src/templates/base.html`. Update the `<form>` `action` URL to point to your email provider (like Mailchimp or ConvertKit).
