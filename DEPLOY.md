# Deploy checklist — get a shareable link (e.g. for LinkedIn)

Do these steps once. After that, your app is live and you can share the link everywhere.

---

## Step 1: Push this project to GitHub

- **If you haven’t pushed yet:** follow **[GITHUB_PUSH.md](GITHUB_PUSH.md)** (create repo on GitHub, then run the `git remote` and `git push` commands).
- **Quick option:** run `push_to_github.bat YOUR_USERNAME YOUR_REPO` (e.g. `push_to_github.bat johndoe quantum-fi`).

Your code is then “official” on GitHub.

---

## Step 2: Deploy the app on Streamlit Cloud (free)

1. Go to **[https://share.streamlit.io](https://share.streamlit.io)**.
2. Sign in with **GitHub**.
3. Click **“New app”**.
4. **Repository:** select your repo (e.g. `YOUR_USERNAME/quantum-fi`).
5. **Branch:** `main`.
6. **Main file path:** `app.py`.
7. Click **Deploy**. Wait a few minutes.
8. Copy the **app URL** (e.g. `https://quantum-fi-xxxxx.streamlit.app`). This is your **shareable link**.

Streamlit Cloud uses your `requirements.txt` automatically.

---

## Step 3: Add the link to GitHub and share it

1. **README:** In [README.md](README.md), replace  
   `[Add your Streamlit Cloud link here after deploy — see DEPLOY.md]`  
   with your real link (e.g. `https://quantum-fi-xxxxx.streamlit.app`).
2. **GitHub repo:** In your repo’s **About** (gear icon), set **Website** to that same link so it shows on the repo page.
3. **LinkedIn (or anywhere):** Post the same link so people can open and use the app in their browser.

---

## Optional: Hugging Face Spaces

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces).
2. Choose **Streamlit** SDK.
3. Add `app.py`, `requirements.txt`, and `pulse_comparison.py` (and any other files the app imports).
4. Use the Space URL as your shareable link instead of (or in addition to) Streamlit Cloud.
