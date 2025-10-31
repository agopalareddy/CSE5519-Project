# Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

The project uses a `.env` file to manage API keys and settings.

**Option A: Use Mock Mode (No API keys needed)**

The `.env` file is already configured for mock mode. Just run:

```bash
python test_phase1.py
python test_phase2.py
```

**Option B: Use Real VLM APIs**

1. Copy the example file (if needed):
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   # For OpenAI GPT-4V
   OPENAI_API_KEY=sk-proj-your-key-here
   VLM_PROVIDER=openai

   # OR for Anthropic Claude
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   VLM_PROVIDER=anthropic
   ```

3. Save and run your code!

### 3. Verify Configuration

```bash
python config.py
```

This will show your current configuration (API keys are hidden for security).

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | (empty) |
| `ANTHROPIC_API_KEY` | Anthropic API key | (empty) |
| `VLM_PROVIDER` | Which VLM to use: `openai`, `anthropic`, or `mock` | `mock` |
| `VLM_MODEL` | Specific model to use (optional) | Provider defaults |
| `MAX_API_CALLS` | Maximum API calls per experiment | `100` |
| `ATTACK_TEMPERATURE` | Temperature for attack generation (0-2) | `0.9` |
| `DEFENSE_TEMPERATURE` | Temperature for defense generation (0-2) | `0.3` |

## Getting API Keys

### OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-`)
5. Add to `.env`: `OPENAI_API_KEY=sk-proj-...`

**Models available:**
- `gpt-4-vision-preview` (default)
- `gpt-4-turbo`
- `gpt-4o`

### Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new key
5. Copy the key (starts with `sk-ant-`)
6. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

**Models available:**
- `claude-3-opus-20240229` (default, most capable)
- `claude-3-sonnet-20240229` (balanced)
- `claude-3-haiku-20240307` (fastest)

## Security Notes

⚠️ **IMPORTANT:**
- **Never commit `.env` to git!** It contains secret API keys
- The `.env` file is already in `.gitignore`
- Always use `.env.example` as a template (no real keys)
- Keep your API keys private

## Cost Management

### Mock Mode (Free)
- No API calls
- Simulated responses
- Perfect for development and testing

### Real API Mode (Costs Money)
- OpenAI: ~$0.01-0.03 per image + text request
- Anthropic: ~$0.01-0.08 per image + text request
- Use `MAX_API_CALLS` to limit costs
- Monitor usage in your provider dashboard

## Testing Your Setup

### Test Mock Mode
```bash
python config.py
python test_phase1.py
python test_phase2.py
```

### Test Real API
```bash
# 1. Configure .env with your API key
# 2. Run a simple test
python stuart/vlm_interface.py

# 3. Run full tests (this will make API calls!)
python test_phase2.py
```

## Troubleshooting

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "No OpenAI/Anthropic API key found"
- Check that `.env` file exists in project root
- Verify your API key is correctly set in `.env`
- Make sure there are no spaces around the `=` sign
- Verify `VLM_PROVIDER` matches your API key

### "API key is invalid"
- Verify you copied the entire key
- Check that the key hasn't been revoked
- Try generating a new key from the provider

### Mock mode when you want real API
- Check `VLM_PROVIDER` in `.env`
- Verify the API key is actually set
- Run `python config.py` to see current configuration

## Project Structure

```
CSE5519 Project/
├── .env                    ← Your API keys (never commit!)
├── .env.example            ← Template (safe to commit)
├── config.py               ← Configuration manager
├── requirements.txt        ← Dependencies
├── SETUP.md               ← This file
└── ...                     ← Other project files
```

## Next Steps

After setup:
1. ✅ Run `python config.py` to verify
2. ✅ Run `python test_phase1.py` to test data pipeline
3. ✅ Run `python test_phase2.py` to test full system
4. ✅ Start development!
