# RobertSawyer.co Site Prototype

Static HTML/CSS/JS lead-conversion site for RobertSawyer.co.

## Strategy

- `RobertSawyer.co` = public lead conversion hub
- `RelationSync.co` = paid/client coaching hub
- Primary CTA = free lead magnet / Kit opt-in
- Secondary CTA = Start Here

## Pages

- `index.html` — conversion-focused homepage
- `free.html` — free lead magnet page with Kit embed placeholders
- `start.html` — choose-your-path page
- `work-with-me.html` — coaching overview and RelationSync application path
- `courses.html` — mini-course/self-paced path

## Local Preview

```bash
python3 -m http.server 8080 --bind 0.0.0.0
```

Open:

```text
http://localhost:8080
```

## GitHub Workflow

Recommended branches:

- `main` — stable/approved live branch
- `draft/homepage-redesign` — Jim's working branch for revisions

Recommended publishing rule:

- Do not enable GitHub Pages on the draft branch.
- Review changes on the working branch or local preview.
- Merge to `main` only when ready to publish.
