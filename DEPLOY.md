# Deploying PagePal (Railway)

**Last updated:** 2025‑08‑12

## 0) Preflight (local)

- **Branch state**
  ```bash
  git checkout mvp && git pull
  # If fixes are on main:
  git merge main   # or: git cherry-pick <SHA>
  git push origin mvp
