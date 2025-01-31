# code-analysis-prompter

- Set `OPENAI_API_KEY` in `.env` (gitignored)
- Place source files to be analyzed in a `files` directory (gitignored)
- Adjust script as needed; currently it's taking Python modules and asking GPT to scan them for top-level code that would execute on import

Then...

```bash
uv run main.py
```
