# Ryan Rickevicius Portfolio

Starter repository for Ryan's sports, data, and business analytics portfolio.

## Current status

This repository contains a simple static starter page and journal publishing examples. The full portfolio design, Hugo templates, browser editor, and scheduled publishing are the next implementation stage. GitHub Pages has not been enabled as part of repository creation.

## Repository contents

- `index.html`: responsive starter page.
- `.nojekyll`: serves the starter directly through GitHub Pages.
- `templates/journal/index.md`: draft-first Markdown article template.
- `docs/hugo-deploy.example.yml`: example Hugo build and scheduled GitHub Pages deployment workflow. This is documentation, not an active workflow.
- `.gitignore`: excludes generated output, local dependencies, and environment files.

## Turn on the starter with GitHub Pages

In this repository, open **Settings → Pages**. Select **Deploy from a branch**, choose **main** and **/(root)**, and save. Once GitHub finishes deploying, the personal site address will be:

https://ryan-rickevicius.github.io/

The repository name follows GitHub's personal-site naming convention. The URL above is the intended website address, not confirmation of a live deployment.

## Planned portfolio

- Home, selected work, Analytics Journal, About, and Contact.
- Hugo-generated pages with the agreed navy-and-teal editorial design.
- Pages CMS for writing articles, uploading charts and PDFs, editing profile content, and updating the resume through a browser.
- Support for written analysis and configured interactive chart or dashboard embeds.
- GitHub Actions checks for scheduled posts every 15 minutes. Scheduled runs are best effort.
- Real research and shareable analytical outputs, with no invented results.

When the Hugo website is implemented, change the Pages publishing source to **GitHub Actions** and install the verified deployment workflow under `.github/workflows/`. The example workflow requires a complete Hugo project and configured Pages publishing before activation.

## Posting workflow after the full build

Open the browser editor, create a post, write or paste the analysis, add its charts and deliverables, select a publication date, mark it ready, and save. Ordinary publishing should not require website code.

Draft and scheduled files in a public repository are readable in the repository even before website publication. Keep confidential or embargoed material out of public source.

## References

- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Hugo](https://gohugo.io/)
- [Pages CMS](https://pagescms.org/)

