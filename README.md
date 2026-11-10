# OlistIQ

Welcome to **OlistIQ** – a quick overview of the project, how to run it locally, and how to share a live demo with others.

---

## 📂 Project Structure

```
OlistIQ/
├─ src/                # Source code (your existing files)
├─ notebooks/          # Jupyter notebooks, if any
├─ requirements.txt    # Python dependencies
├─ app.py              # Simple Streamlit demo (optional)
├─ docs/               # Markdown docs for GitHub Pages / MkDocs
├─ screenshots/        # Screenshots for the README
└─ README.md           # This file
```

## ✅ Why only 4 files appear on GitHub?

If you see only a handful of files on GitHub, the most common reasons are:
1. **Uncommitted files** – they exist locally but haven’t been `git add`‑ed.
2. **Ignored by `.gitignore`** – a rule is skipping them.

Run the following in the project folder to verify:

```bash
# Show what Git sees (including ignored files)
git status --ignored

# Add everything that isn’t ignored
git add .

git commit -m "Add all project files"

git push origin main   # or the branch you use
```

If you discover a rule that’s unintentionally ignoring files, edit `.gitignore` (or add a negation like `!src/your_file.py`).

---

## 🚀 Quick Live Demo with Streamlit (Python only)

If you have a Python codebase, you can spin up a tiny web UI in minutes using **Streamlit**.

### 1. Install Streamlit

```bash
pip install streamlit
```

### 2. Add a demo script (`app.py`)

A minimal example is provided in this repo. It loads the main function from `src/main.py` (replace with your entry point) and displays the output.

```python
# app.py
import streamlit as st

# Import your project’s main logic – adjust the import path as needed
# from src.main import run

def run():
    return "Hello from OlistIQ! Replace this with your real function."

st.title("OlistIQ Demo")
st.write(run())
```

### 3. Run locally

```bash
streamlit run app.py
```

A browser window opens at `http://localhost:8501` showing the UI.

### 4. Deploy for free

- **Streamlit Community Cloud** – Connect your GitHub repo and click *“Deploy”*. It will automatically build and serve the app at a public URL.
- **Netlify / Vercel** – If you have a Node/React front‑end, link the repo and let the platform handle the build.

---

## 📚 Documentation Site (GitHub Pages)

If you prefer a static site (e.g., API docs, screenshots, usage guide), enable **GitHub Pages**:
1. Create a `docs/` folder.
2. Add Markdown files there (e.g., `docs/overview.md`).
3. In GitHub → *Settings* → *Pages*, select the `docs/` folder as the source.
4. Push the changes – GitHub will publish at `https://<username>.github.io/<repo>/`.

---

## 📸 Screenshots

Place any images you want to showcase in the `screenshots/` directory and reference them like this:

```markdown
![Main screen](screenshots/main.png)
![Feature view](screenshots/feature.png)
```

> **Tip:** The two PNGs you uploaded can be copied into `screenshots/`.

---

## 📦 Optional – Docker container

For a reproducible environment, add a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]
```

Build and run:
```bash
docker build -t olistiq .
docker run -p 8501:8501 olistiq
```

---

## 🎉 Next Steps
1️⃣ Ensure **all** project files are committed and pushed.  
2️⃣ Pick a sharing method (Streamlit demo, GitHub Pages, Docker, etc.).  
3️⃣ Add the `screenshots/` folder and place your images there.  
4️⃣ Update the `README.md` (you’re already looking at it!).

Feel free to ask me to:
- Create a skeleton `Dockerfile`.
- Generate a more detailed `app.py` that calls a specific function from your code.
- Write a sample MkDocs `mkdocs.yml` for a full‑featured docs site.
- Anything else you need!
