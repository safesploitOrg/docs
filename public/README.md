# Public static search page

## What is this?

safesploitOrg/docs/ searchable via 
https://safesploitorg.github.io/docs/

## Why not use Hugo?

Hugo is in the pipeworks, additionally this repo is not my source-of-truth for documentation.


---

# Public Static Search Page

## What is this?

This directory contains the static GitHub Pages front-end for the `safesploitOrg/docs` repository.

<a href="https://safesploitorg.github.io/docs/
">GitHub Page</a>

## Why not use Hugo?

Hugo is planned for a future version of the documentation site.

For now, this static page is intentionally simple:

* no build framework
* no backend (easy deployment through GitHub Pages)
* no external service dependency

This repository is also not the primary source of truth for my documentation. The source of truth remains my internal Confluence/Obsidian/knowledge base, with this repo acting as a public-safe documentation mirror and portfolio-facing reference.


## How search works

The GitHub Actions workflow generates:

```text
public/search-index.json
```

The static page then loads that JSON file in the browser and searches across indexed Markdown content from the repository.

## Deployment

GitHub Pages deploys the contents of this directory:

```yaml
path: ./public
```

So `public/index.html` becomes the homepage for the published site.
