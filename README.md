# Ryan Rickevicius Portfolio

Sports, data, and business analytics portfolio with an Analytics Journal.

## Website and editor

- Website: https://ryan-rickevicius.github.io/
- Content editor: https://app.pagescms.org/
- Repository: https://github.com/Ryan-Rickevicius/Ryan-Rickevicius.github.io

Sign into Pages CMS with GitHub, open this repository and its main branch, and choose **Analytics Journal** to add a post. The one-time GitHub App connection needs the repository owner's authorization. See the [content guide](docs/CONTENT-GUIDE.md) for step-by-step instructions and supported file and embed formats.

## Routine updates

1. Create an article, enter a title and summary, and write or paste the content.
2. Upload charts or reports. Add supported interactive embed URLs in Article details when needed.
3. Choose the publication date and time in Eastern Time.
4. Keep **Draft** on while writing. Turn it off when ready, then save.

Saving updates GitHub. A successful build publishes eligible content. The workflow checks every 15 minutes at minutes 7, 22, 37, and 52. GitHub schedules may be delayed and public-repository schedules can pause after 60 days without activity. Images, PDFs, and interactive outputs use the same article styling automatically. A public repository also exposes draft source files before website publication.

The editor also supports Homepage, Selected work, About, Contact, and Profile, experience and resume. The public resume can be replaced through the editor. A custom interactive feature beyond the supported embeds may need a one-time integration.

## Preview a draft

In GitHub open **Actions → Preview drafts → Run workflow**. Download the draft-website-preview artifact from the completed run. Unzip it and open index.html. It includes draft and scheduled posts and is not the published website. Production deployment always excludes drafts and future posts.

## Local development

The project uses Hugo 0.169.0 and has no Node package dependency. With Hugo installed, run `hugo server` from this folder. Use `hugo server --buildDrafts --buildFuture` to inspect unfinished content locally. Validate content with `python3 scripts/validate_content.py .` before building. Ruby is used only for its standard YAML parser during validation.

The **Publish portfolio** workflow validates content, builds static HTML, and deploys it to GitHub Pages. Configure **Settings → Pages → Source: GitHub Actions**. No server, database, or paid domain is required.

## Content structure

- `content/blog/`: Markdown articles and optional page bundles.
- `content/projects/`: curated case studies.
- `data/profile.yaml`: biography, contact information, education, experience and tools.
- `assets/uploads/`: article files, published only when referenced by an eligible page.
- `static/resume/`: the public resume PDF.
- `layouts/` and `assets/css/`: the shared website design.
- `.pages.yml`: browser editor configuration.

The pitch-location illustration is a schematic. Research results are described only to the extent supported by the supplied resume. Add the original poster, figures and shareable reports through the editor when ready.
