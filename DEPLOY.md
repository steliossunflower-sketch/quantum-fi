# Deploy to Streamlit Cloud / Hugging Face

## Streamlit Cloud (share.streamlit.io)

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. New app -> select repo, branch, main file: `app.py`
5. Streamlit Cloud uses `requirements.txt` automatically

## Hugging Face Spaces

1. Create new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose "Streamlit" SDK
3. Add `app.py` and `requirements.txt`
4. Add `pulse_comparison.py` (imported by app)
