# Publishing and Updating Your Portfolio

Use the browser editor for ordinary updates. It saves Markdown and uploaded files to GitHub, and the website applies the same design to every article.

## Connect the editor once

1. Open [Pages CMS](https://app.pagescms.org/) and sign in with your GitHub account.
2. Install or authorize Pages CMS for **Ryan-Rickevicius.github.io**. Choose access to this repository when GitHub offers a repository selection.
3. Open that repository on the **main** branch. The supplied `.pages.yml` configures the editing screens.
4. Confirm that Analytics Journal, Selected work, About page, Contact page, and Profile, experience and resume are listed.

This account connection requires your GitHub sign-in and authorization. Having the configuration in the repository does not itself grant the editor access. No separate content database or paid hosting plan is needed for this setup.

## Write a journal article

1. Open **Analytics Journal** and choose **New**.
2. Enter a title and a short preview summary. The editor creates the filename from the title automatically. Keep the article’s address stable once it is published.
3. Choose a publication date and time in **Eastern Time**. The site uses America/New_York, including daylight saving time. Enter the intended Eastern wall-clock time even if you are travelling.
4. Keep **Keep as draft** switched on while working.
5. Write or paste into **Article**. Use the toolbar for headings, links, lists, images, tables, and formatted code where supported by the editor. Source mode is available for an existing Markdown article, but routine posting does not require it.
6. Add topics and the tools used. Upload a cover image only when it helps describe the work, and supply its image description.
7. Add reports or data under **Downloadable reports and data**. Give each file a readable button label.
8. Add any supported chart or dashboard under **Interactive charts and dashboards**.
9. Save. Review the content preview and use the repository's draft-preview workflow when you need to see the actual website layout before publication.
10. When ready, turn **Keep as draft** off and save. A due article publishes after the next successful build and deployment.

The browser editor's own preview shows content editing. The built website or downloadable draft preview is the reference for final styling. New editor-created posts are stored directly in `content/blog/` as a Markdown file; folder-based articles are supported too. You do not need to arrange folders yourself.

## Schedule or publish immediately

**Draft:** Keep as draft is on. The article is excluded from production even if its date has passed.

**Scheduled:** Draft is off and the publication time is in the future. The article appears after the first successful deployment at or after that time.

**Publish now:** Draft is off and the publication date is now or in the past. Saving triggers the normal build.

The workflow also checks every 15 minutes. GitHub can delay or drop scheduled runs, so publication is approximate and includes build time. Public-repository schedules can be disabled after 60 days without repository activity. If a due post has not appeared, check the **Actions** tab, re-enable a disabled workflow if needed, and run **Publish portfolio** manually.

Saving is the step that sends your edits to GitHub. An article left open with unsaved changes will not publish.

## Add charts and downloadable files

Use the image button in the Article editor for figures. Add useful alternative text describing the chart, and explain the important result in nearby prose. Under Article details, a cover caption can credit the source or clarify what the visual shows.

Upload PDFs, CSVs, spreadsheets, ZIPs, or text files through the download fields. Uploaded article files are stored under `assets/uploads/`. The website publishes resources when a published article references them. Keep scheduled files out of `static/`, which is reserved for assets that may be public immediately.

The repository itself is public. Draft article text and files committed to it can be read in GitHub before they appear on the website. Keep private team material and embargoed work outside this public repository until they may be shared.

## Add an interactive chart or dashboard

Publish the visualization through its provider first. Then add a title, the supported URL, and a short explanation under **Interactive charts and dashboards**. Paste a URL, rather than a block of embed code.

Supported URL shapes:

- **Datawrapper:** `https://datawrapper.dwcdn.net/CHARTID/1/`. Use its **Visualization only** URL, including the current version number.
- **Flourish:** `https://flo.uri.sh/visualisation/123456/embed` or the equivalent `/story/123456/embed` URL from the iframe option.
- **Tableau Public:** `https://public.tableau.com/views/Workbook/View` or a `/shared/` URL. Use a published public view that can be viewed without signing in.

The website adds the surrounding layout, title, external-open link, and caption. A provider may have its own publishing restrictions or plan limits. If an embed is unavailable, readers can still use the external-open link and the article's written explanation. Flourish iframe embeds retain a visible provider credit.

New custom interactions or a provider outside this list need a one-time integration. Updating a supported existing chart or swapping its URL does not require website code. Creating the analysis itself remains part of your analytical work.

## Update other pages

- **Homepage:** Edit the main headline and small heading above it. The Profile screen holds the main introduction; Additional introduction is optional extra text.
- **Selected work:** Edit the case-study title, summary, article, organization, role, period, cover image, reports, and supported embeds. The Main question, Analytical approach, and Data and project context fields supply the homepage's featured-project notes. Display order puts smaller numbers first. If several projects have Featured enabled, the lowest display-order number is used for the main homepage feature.
- **About page:** Edit the main headline and biography through labeled fields.
- **Contact page:** Edit the main headline and introductory text. Change email and social links in the Profile screen.
- **Profile, experience and resume:** Update the homepage introduction, internship interest, contact links, education, experience, skill groups, interests, or public resume PDF.

Keep personal addresses and phone numbers out of the public profile unless you deliberately decide to publish them. The public resume is intended to contain professional contact details.

## Optional Markdown route

Existing Markdown articles can still be added through GitHub or a local editor. The `archetypes/blog.md` file is a draft-first template. Use top-level fields for title, summary, publishDate, draft, and tags. Keep optional website-specific fields under `params`.

For hand-written dates, use an ISO timestamp with a correct offset, such as `2026-11-02T09:00:00-05:00`, or an Eastern wall-clock timestamp without an offset, such as `2026-11-02T09:00:00`. Offset-free times use the site's America/New_York setting. Avoid copying a winter numeric offset onto a summer date.

## Sources and maintenance

The editor configuration follows the official [Pages CMS quick start](https://pagescms.org/docs/quick-start/), [field configuration](https://pagescms.org/docs/configuration/content/fields/), [date picker](https://pagescms.org/docs/configuration/fields/date/), [rich-text editor](https://pagescms.org/docs/configuration/fields/rich-text/), and [media configuration](https://pagescms.org/docs/configuration/media/).

Embed formats follow [Datawrapper's sharing guide](https://www.datawrapper.de/academy/how-to-embed-charts), [Flourish's CMS embedding guide](https://helpcenter.flourish.studio/hc/en-us/articles/8761537208463-How-to-embed-Flourish-charts-in-your-CMS), and [Tableau's sharing guide](https://help.tableau.com/current/pro/desktop/en-us/shareworkbooks.htm).
