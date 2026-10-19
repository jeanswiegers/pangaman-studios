#!/usr/bin/env python3
"""Builds the static Pangaman Studios site into this folder (plain HTML, no scripts).

Usage: python3 build.py   (needs the `markdown` package; /workspace/.venv-docs has it)
The manual and changelog are copied from ../coreclr-ready/docs/package/ when that folder exists, so the site
always shows the shipped text; otherwise the copies in content/ are used.
Placeholders in CAPITALS (e.g. SUPPORT_EMAIL) must be replaced before publishing; see README.md."""
import html, os, re, shutil
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_DOCS = os.path.join(HERE, "..", "coreclr-ready", "docs", "package")
UPDATED = "19 October 2026"

PH = ["ASSET_STORE_LITE_URL", "ASSET_STORE_PRO_URL", "ASSET_STORE_PUBLISHER_URL", "SUPPORT_EMAIL", "SUPPORT_REPLY_TIME", "SITE_URL"]


def ph(name):
    return '<span class="placeholder">' + name + "</span>"


NAV = [("index.html", "Home"), ("coreclr-ready.html", "CoreCLR Ready"), ("docs.html", "Documentation"),
       ("changelog.html", "Changelog"), ("support.html", "Support")]


def page(file, title, body, description):
    nav = "".join('<li><a href="{0}"{1}>{2}</a></li>'.format(h, ' aria-current="page"' if h == file else "", t) for h, t in NAV)
    full_title = title + " · Pangaman Studios" if title != "Pangaman Studios" else title
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self'; style-src 'self'; script-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="brand" href="index.html"><img src="assets/img/mark.svg" alt="" width="36" height="36">Pangaman Studios</a>
<nav class="main" aria-label="Main"><ul>{nav}</ul></nav>
</div></header>
<main id="main"><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
<p>© 2026 Pangaman Studios. Unity is a trademark of Unity Technologies; this site is not affiliated with or endorsed by Unity.</p>
<ul><li><a href="privacy.html">Privacy</a></li><li><a href="how-we-build.html">How we build</a></li><li><a href="support.html">Contact</a></li><li><a href="changelog.html">News</a></li></ul>
</div></footer>
</body>
</html>
"""
    for p in PH:  # visible placeholder in text, raw token in attributes
        out = re.sub(r"(?<![\"'=:/A-Z_])" + p + r"(?![A-Z_\"'])", ph(p), out)
    with open(os.path.join(HERE, file), "w", encoding="utf-8") as f:
        f.write(out)


def md(text):
    m = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"], extension_configs={"toc": {"toc_depth": "2-3"}})
    return m.convert(text), m.toc


def source(name):
    src = os.path.join(PKG_DOCS, name)
    dst = os.path.join(HERE, "content", name)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
    with open(dst, encoding="utf-8") as f:
        return f.read()


def shot(name, alt, caption):
    base = "assets/img/" + name
    return (f'<figure><a href="{base}.png"><img src="{base}-800.png" alt="{html.escape(alt)}" width="800" height="480" loading="lazy"></a>'
            f"<figcaption>{caption}</figcaption></figure>")


def home():
    body = f"""
<section class="hero">
<div>
<img class="mark" src="assets/img/mark.svg" alt="" width="72" height="72">
<h1>Pangaman Studios</h1>
<p class="lead">A small, independent publisher of Unity editor tools. We build focused tools for one job each,
explain what they do and what they don't, and keep them working as Unity changes.</p>
<div class="btns"><a class="btn" href="coreclr-ready.html">CoreCLR Ready</a><a class="btn ghost" href="support.html">Get help</a></div>
</div>
<div><figure><a href="assets/img/02-ccr001-diff-preview-dark.png"><img src="assets/img/crop-diff.png" alt="Part of the CoreCLR Ready window: a static singleton finding with a diff preview of the generated reset method and an Apply this fix button." width="872" height="600"></a><figcaption>CoreCLR Ready showing a finding and the preview of its fix (Pro).</figcaption></figure></div>
</section>

<h2>Tools</h2>
<div class="cards">
<div class="card pro">
<h3><a href="coreclr-ready.html">CoreCLR Ready</a></h3>
<p>Finds the C# code in a Unity project that breaks when Domain Reload is turned off and when the project moves to
Unity's CoreCLR scripting runtime, and shows the change each problem needs. Available as a free Lite edition
(scan and preview) and a Pro edition (apply fixes with backup and undo).</p>
<p><a href="coreclr-ready.html">About CoreCLR Ready</a> · <a href="docs.html">Manual</a></p>
</div>
<div class="card">
<h3>How we work</h3>
<ul>
<li>Editor-only tools. Nothing is added to your player builds.</li>
<li>No telemetry, no accounts, no network calls. See the <a href="privacy.html">privacy policy</a>.</li>
<li>We test on the Unity versions we list, and say plainly which ones we haven't tested.</li>
<li>Built with AI assistance and reviewed by a person. <a href="how-we-build.html">More about that</a>.</li>
</ul>
</div>
</div>

<h2>News</h2>
<p>CoreCLR Ready 0.1.0 is being prepared for the Unity Asset Store. Release notes appear in the
<a href="changelog.html">changelog</a> as versions ship.</p>
"""
    page("index.html", "Pangaman Studios", body, "Pangaman Studios is a small independent publisher of Unity editor tools.")


def product():
    body = f"""
<section class="hero">
<div>
<h1>CoreCLR Ready</h1>
<p class="lead">Find the code that breaks with Domain Reload off and on CoreCLR, and see the fix before anything changes.</p>
<p>Unity is moving from Mono to the CoreCLR runtime, and turning off Domain Reload in Enter Play Mode Options
makes entering Play mode faster (from Unity 6.8 it is the only option). Both changes break code that used to work: static fields
keep their values between Play sessions, <code>AppDomain</code> APIs stop behaving the same, <code>BinaryFormatter</code>
goes away. CoreCLR Ready scans your project's C# for these patterns, explains each one, links to Unity's
documentation and, where a safe mechanical change exists, shows the exact edit as a diff.</p>
<div class="btns"><a class="btn" href="ASSET_STORE_LITE_URL">Get Lite (free)</a><a class="btn" href="ASSET_STORE_PRO_URL">Get Pro</a><a class="btn ghost" href="docs.html">Read the manual</a></div>
</div>
<div><figure><a href="assets/img/01-findings-list-dark.png"><img src="assets/img/crop-list.png" alt="Findings list grouped by file after a scan of a demo project, with warning and error icons and [fix] tags." width="760" height="560"></a><figcaption>Findings grouped by file after a scan. <code>[fix]</code> marks findings with an automatic fix.</figcaption></figure></div>
</section>

<h2>Lite and Pro</h2>
<div class="cards">
<div class="card lite">
<h3>Lite (free)</h3>
<ul>
<li>Scans <code>Assets/</code> and embedded or local packages with the same defines and references Unity uses.</li>
<li>Eleven rules (CCR001–CCR011) with explanations and links to Unity's documentation.</li>
<li>Diff preview of every automatic fix.</li>
<li>JSON and Markdown reports; batchmode command with a CI exit code.</li>
<li>Read-only: Lite never changes your files.</li>
</ul>
<a class="btn" href="ASSET_STORE_LITE_URL">Asset Store: Lite</a>
</div>
<div class="card pro">
<h3>Pro</h3>
<ul>
<li>Everything in Lite.</li>
<li>Apply one fix or all fixes after reviewing the preview.</li>
<li>Automatic backup of every changed file, and one-click <strong>Revert last</strong> that refuses to overwrite later edits.</li>
<li>Command-line apply and revert for CI.</li>
<li>Scan of precompiled managed DLLs (detect-only).</li>
</ul>
<a class="btn" href="ASSET_STORE_PRO_URL">Asset Store: Pro</a>
</div>
</div>

<h2>What it checks</h2>
<p>Mutable static state that survives Play mode with Domain Reload off (fields, events, auto-properties,
singletons), <code>AppDomain.GetAssemblies</code> and <code>DomainUnload</code>, <code>BinaryFormatter</code>,
<code>Assembly.Location</code>, pointer-to-int conversions, <code>string.GetHashCode</code> used as a stable value,
non-default encodings, <code>Assembly.LoadFile</code>/<code>LoadFrom</code>, <code>ManagedDebugger</code> and
<code>[DllImport]</code> into Mono runtime libraries. The <a href="docs.html#4-rules">rules table</a> in the manual
lists which ones have an automatic fix.</p>
<p>The analysis is static: it can't know whether a static value is meant to persist. Those cases are reported, not
fixed, and you can silence one with a comment.</p>

<h2>Screenshots</h2>
<div class="shots">
{shot("02-ccr001-diff-preview-dark", "A static singleton finding with the diff preview of a generated reset method and the Apply this fix button.", "Pro: a static singleton finding and the generated reset method, ready to apply.")}
{shot("03-ccr004-manual-change-dark", "A BinaryFormatter error with the recommendation and a note that a manual change is needed.", "Some problems need a person: BinaryFormatter is reported with the reason and no automatic fix.")}
{shot("04-pro-after-apply-dark", "The window after applying a fix: the status line names the backup folder and Revert last is enabled.", "Pro after applying a fix: the backup location is shown and Revert last is available.")}
{shot("05-pro-after-revert-dark", "The window after Revert last: the status line reports the reverted fix and the findings are back.", "Pro after Revert last.")}
{shot("06-lite-diff-preview-dark", "Lite showing the same diff preview with a note that Lite does not apply changes.", "Lite shows the same preview; you apply the change yourself.")}
{shot("07-ccr001-diff-preview-light", "The window in Unity's light editor theme.", "Light editor theme.")}
</div>

<h2>Compatibility</h2>
<table>
<thead><tr><th scope="col">Area</th><th scope="col">Status</th></tr></thead>
<tbody>
<tr><td>Unity versions</td><td>6000.0 or newer. Tested on <strong>6000.0.85f1 (LTS)</strong> and <strong>6000.6.6f1</strong>.
6000.1 to 6000.5 and 6000.7 have not been tested yet.</td></tr>
<tr><td>Editor platforms</td><td>Tested in the Linux editor (window, batchmode, tests, apply/revert). Windows and macOS editors not tested yet.</td></tr>
<tr><td>Player builds</td><td>Not affected: editor-only, nothing is added to builds.</td></tr>
<tr><td>Render pipelines</td><td>Not applicable (no runtime content).</td></tr>
<tr><td>Dependencies</td><td>Lite: none. Pro: Unity's <code>com.unity.nuget.mono-cecil</code> package (installed automatically) and Lite.</td></tr>
</tbody>
</table>
"""
    page("coreclr-ready.html", "CoreCLR Ready", body, "CoreCLR Ready finds Unity C# code that breaks with Domain Reload off and on CoreCLR, and previews the fix.")


def docs():
    text = source("Manual.md")
    body_html, toc = md(text)
    body = f"""<div class="doc">
<nav class="toc" aria-label="Manual contents"><strong>Contents</strong>{toc}<p><a href="assets/coreclr-ready-manual.pdf">Download as PDF</a></p></nav>
<article class="prose">{body_html}</article>
</div>"""
    page("docs.html", "CoreCLR Ready manual", body, "User manual for CoreCLR Ready Lite and Pro.")


def changelog():
    text = source("CHANGELOG.md")
    text = re.sub(r"^# .*\n", "", text, count=1)
    body_html, _ = md(text)
    body = f"""<h1>Changelog and news</h1>
<p class="lead">Release notes for our tools, newest first. Versions marked “unreleased” are in preparation.</p>
<h2>CoreCLR Ready</h2>
<div class="prose">{body_html.replace("<h2", "<h3").replace("</h2>", "</h3>")}</div>
<h2>Site</h2>
<ul><li>{UPDATED}: site created.</li></ul>
"""
    page("changelog.html", "Changelog", body, "Release notes and news for Pangaman Studios tools.")


def support():
    body = f"""<h1>Support</h1>
<p class="lead">Questions, bug reports and feature requests are welcome. A person reads every message.</p>
<h2>Contact</h2>
<p>Email <a href="mailto:SUPPORT_EMAIL">SUPPORT_EMAIL</a>. We usually reply within SUPPORT_REPLY_TIME.</p>
<p>You can also reach us through our <a href="ASSET_STORE_PUBLISHER_URL">publisher page on the Unity Asset Store</a>.</p>
<h2>What to include</h2>
<ul>
<li>The product and edition (Lite or Pro) and its version (Package Manager shows it).</li>
<li>Your Unity version and editor platform (Windows, macOS or Linux).</li>
<li>For a wrong or missing finding: the exported Markdown report (<strong>Export MD</strong>), and if you can, a small
code sample that shows it. Please remove anything you don't want to share.</li>
<li>For an error: the lines starting with <code>[CoreCLR Ready]</code> from the Console or <code>Editor.log</code>.</li>
</ul>
<h2>Before you write</h2>
<ul>
<li>The <a href="docs.html">manual</a> covers installation, every rule, the command line, applying and reverting fixes, and known limitations.</li>
<li>If a static value is meant to persist between Play sessions, that's not a bug: put <code>// CoreClrReady:ignore</code>
on the line above it, or mark it <code>[NoAutoStaticsCleanup]</code>.</li>
<li>Pro keeps backups in <code>Library/CoreClrReady/Backups</code>. <strong>Revert last</strong> restores the last batch of fixes.</li>
</ul>
<h2>Refunds and licensing</h2>
<p>Purchases, licences and refunds are handled by the Unity Asset Store under its terms.</p>
"""
    page("support.html", "Support", body, "How to get help with Pangaman Studios tools.")


def privacy():
    body = f"""<h1>Privacy policy</h1>
<p class="muted">Last updated {UPDATED}.</p>
<p class="lead">Short version: our tools collect nothing and send nothing, and this website doesn't track you.</p>
<h2>Our Unity tools</h2>
<p>CoreCLR Ready (Lite and Pro) runs entirely inside your Unity editor. It has no telemetry or analytics and makes no
network connections. It doesn't use accounts or licence checks of its own.</p>
<ul>
<li>It reads your project's C# files (and, in Pro, managed DLLs) to analyse them on your computer.</li>
<li>It writes files only when you ask it to: a report you export, and in Pro the files you choose to fix plus their
backups in your project's <code>Library/CoreClrReady/Backups</code> folder. You can delete those at any time.</li>
<li>The <strong>Unity docs</strong> button opens a Unity documentation page in your web browser when you click it.
That page is Unity's, under Unity's privacy policy.</li>
</ul>
<h2>This website</h2>
<p>This site is static HTML. It uses no cookies, no analytics, no scripts, no web fonts and no content from other
sites. It is hosted on GitHub Pages; GitHub may process technical data such as your IP address to deliver the
pages, as described in the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub
Privacy Statement</a>.</p>
<h2>Purchases</h2>
<p>Our tools are sold through the Unity Asset Store. Unity handles payment and your account; we receive the
information Unity shares with publishers under its terms, and use it only for licensing and support.</p>
<h2>When you contact us</h2>
<p>If you email us, we use your address and message only to reply and to fix the problem you report. We don't add
you to mailing lists and don't share your messages. Ask us at any time to delete them:
<a href="mailto:SUPPORT_EMAIL">SUPPORT_EMAIL</a>.</p>
<h2>Changes</h2>
<p>If this policy changes, the new version will be posted here with a new date.</p>
"""
    page("privacy.html", "Privacy policy", body, "Pangaman Studios tools collect no data and make no network calls.")


def ai():
    body = """<h1>How we build</h1>
<p class="lead">Our tools are built with AI assistance and reviewed by a person.</p>
<p>We use AI coding assistants to help write code, tests and documentation. A person at Pangaman Studios decides
what each tool should do, reviews the changes, and is responsible for what we ship.</p>
<p>What that means in practice:</p>
<ul>
<li>Every rule ships with automated tests against real Unity versions, and those tests must pass before a release.</li>
<li>Automatic fixes are conservative: when a change could alter behaviour, the tool reports the problem instead of
fixing it. In Pro, fixes are shown as a diff before anything changes, backed up, and can be reverted.</li>
<li>Screenshots on this site are real captures of the tool. Marketing images are designed from those captures.</li>
<li>If something is wrong, it's our mistake to fix. Please <a href="support.html">tell us</a>.</li>
</ul>
"""
    page("how-we-build.html", "How we build", body, "Pangaman Studios tools are built with AI assistance and reviewed by a person.")


def notfound():
    page("404.html", "Page not found", '<h1>Page not found</h1><p>That page doesn\'t exist. Try the <a href="index.html">home page</a>.</p>', "Page not found.")


if __name__ == "__main__":
    for f in (home, product, docs, changelog, support, privacy, ai, notfound):
        f()
    open(os.path.join(HERE, ".nojekyll"), "w").close()
    print("built")
