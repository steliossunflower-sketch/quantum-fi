# Push this project to GitHub (one-time setup)

Your project is already committed locally. Follow these steps to put it on GitHub.

## Step 1: Create a new repository on GitHub

1. Open **[https://github.com/new](https://github.com/new)** in your browser (you’re already logged in).
2. **Repository name:** e.g. `quantum-fi` or `golden-ratio-quantum-pulse` (no spaces).
3. **Public**, leave **“Add a README”** unchecked (you already have one).
4. Click **Create repository**.

## Step 2: Push your code from this folder

In a terminal (PowerShell or Command Prompt), go to this project folder and run (replace **YOUR_USERNAME** and **YOUR_REPO** with your GitHub username and the repo name you chose):

```bash
cd "c:\Users\User\Documents\quantum fi"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Example: if your username is `johndoe` and repo is `quantum-fi`:

```bash
git remote add origin https://github.com/johndoe/quantum-fi.git
git push -u origin main
```

If Git asks for credentials, use your GitHub username and a **Personal Access Token** (not your password). Create one at: GitHub → Settings → Developer settings → Personal access tokens.

After this, your project is on GitHub and you can deploy it (see **DEPLOY.md**).
