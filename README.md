# Pangaman Studios website (draft, not published)

Plain static HTML/CSS for GitHub Pages. No scripts, cookies, analytics, web fonts or third-party requests
(each page sets a Content-Security-Policy that blocks them).

- Build: `/workspace/.venv-docs/bin/python build.py` (regenerates the `*.html` pages; the manual and changelog
  are copied from `../coreclr-ready/docs/package/` into `content/` when available).
- Previews: `./tools-preview.sh` writes full-page screenshots to `preview/` (desktop 1280 px, plus mobile 390 px
  for Home and CoreCLR Ready).
- Screenshots in `assets/img/` come from `../coreclr-ready/marketing/screenshots/` (real editor captures).

## Placeholders to fill before publishing (search build.py)

| Placeholder | Where | What |
|---|---|---|
| `ASSET_STORE_LITE_URL` | CoreCLR Ready page (2 buttons) | Asset Store URL of the Lite package |
| `ASSET_STORE_PRO_URL` | CoreCLR Ready page (2 buttons) | Asset Store URL of the Pro package |
| `ASSET_STORE_PUBLISHER_URL` | Support | Asset Store publisher page |
| `SUPPORT_EMAIL` | Support, Privacy | Support address (not a personal one) |
| `SUPPORT_REPLY_TIME` | Support | e.g. "two working days" |

Also review before publishing: the "tested on" Unity versions and platforms (CoreCLR Ready page and manual),
the "Last updated" date (`UPDATED` in build.py) and the GitHub Pages hosting paragraph in the privacy policy.

Publishing (not done): a GitHub repository with Pages enabled on the default branch, root folder (`.nojekyll` is
included). A custom domain would need a `CNAME` file.
