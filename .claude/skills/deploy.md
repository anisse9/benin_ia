# Deploy Skill

When the user invokes `/deploy`, run the full git deploy workflow for this project without asking for confirmation.

## Steps

1. Run `git status` to see what has changed.
2. Stage only website files — never stage: zip files (`*.zip`), loose photos not referenced in index.html, or anything inside `.claude/`.
   - Use: `git add index.html` plus any `.png`, `.jpg`, `.svg`, `.ico`, `.css`, `.js` files that appear in `git status` (tracked or untracked).
   - If `.claude/skills/` was updated, include it: `git add .claude/skills/`.
3. Run `git diff --cached --stat` to see what will be committed.
4. Auto-generate a commit message from the staged diff:
   - Look at which files changed and summarize in one short French sentence (this is a French-language project).
   - Example: "Mise à jour du hero et correction du footer"
5. Commit with the generated message, including the Co-Authored-By trailer.
6. Push to `origin master`.
7. Report the result: commit hash + "Déployé sur GitHub Pages."

## Rules

- Never use `--no-verify`.
- Never force-push.
- If nothing is staged after step 2, tell the user "Rien à déployer." and stop.
- Do not ask for confirmation — execute immediately when `/deploy` is typed.
