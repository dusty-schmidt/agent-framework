# 🚀 DEVELOPER SETUP - STANDARDIZED

## API Key Configuration (REQUIRED)

### Step 1: Get Your API Key
1. Go to https://openrouter.ai/
2. Create an account and get your API key
3. Your key will start with `sk-or-`

### Step 2: Configure the API Key
**ONLY ONE PLACE TO PUT IT:**

Edit `config.toml` and replace the placeholder:

```toml
[api]
provider = "openrouter"
base_url = "https://openrouter.ai/api/v1"
api_key = "sk-or-your-actual-key-here"  # <-- PUT YOUR KEY HERE
model = "z-ai/glm-4.5-air"
```

**That's it!** No environment variables, no shell profiles, no conda environments to worry about.

## Quick Start

```bash
# 1. Set your API key in config.toml (see above)
# 2. Start the system
python main.py --test
```

## Development Commands

```bash
# Start test interface (recommended for development)
python main.py --test

# Start standard interface
python main.py

# Start backend only (for debugging)
python backend_api.py

# Check system status
python check_servers.py

# Monitor logs
python scripts/monitor_logs.py -f application
```

## Docker Deployment (Future)

When ready for deployment, the system will use Docker with environment variables:

```dockerfile
ENV OPENROUTER_API_KEY=your_key_here
```

But for development, **always use `config.toml`**.

## Troubleshooting

### "Demo mode active" message?
- Check that your API key is properly set in `config.toml`
- Make sure it starts with `sk-or-`
- Restart the servers after changing the config

### Still having issues?
1. Check `config.toml` has your real API key
2. Run `python check_servers.py` to verify status
3. Check logs: `python scripts/monitor_logs.py -e`

## For New Developers

**DO NOT:**
- Set environment variables
- Modify shell profiles  
- Use conda environments for API keys
- Create .env files

**DO:**
- Put your API key in `config.toml`
- Use the standardized startup commands
- Check this file when in doubt

---

**The API key goes in `config.toml` - period. No exceptions, no alternatives.**
