---
name: stealth-browser
description: "Stealth browser automation via Docker container with OS-level input (undetectable). Use when: (1) scraping sites with anti-bot protection, (2) bypassing 403/rate-limits, (3) need human-like browser behavior, (4) persisting cookies/logins across sessions, (5) user mentions 'stealth browser', 'undetectable scraping', 'bypass 403', 'OS-level click', or 'VNC browser'. Requires Docker container psyb0t/stealthy-auto-browse."
---

# Stealth Browser - Undetectable Web Automation

Docker-based stealth browser with OS-level input (mouse/keyboard) - bypasses bot detection.

## Quick Start

### Container Starten

```bash
docker run -d \
  --name stealth-browser \
  -p 127.0.0.1:8081:8080 \
  -p 127.0.0.1:5901:5900 \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=512m \
  --security-opt=no-new-privileges \
  --cap-drop=ALL \
  -v ~/.openclaw/stealth-browser-profile:/userdata \
  -e TZ=Europe/Berlin \
  psyb0t/stealthy-auto-browse:latest
```

### API Endpoint

```
http://localhost:8081
```

### Health Check

```bash
curl http://localhost:8081/health
# Returns: "ok"
```

## Core Actions

### Navigate

```bash
curl -X POST http://localhost:8081 \
  -H 'Content-Type: application/json' \
  -d '{"action": "goto", "url": "https://example.com"}'
```

### Get Page Text

```bash
curl -X POST http://localhost:8081 \
  -H 'Content-Type: application/json' \
  -d '{"action": "get_text"}'
```

### Find Interactive Elements

```bash
curl -X POST http://localhost:8081 \
  -H 'Content-Type: application/json' \
  -d '{"action": "get_interactive_elements"}'
```

Returns: Buttons, links, inputs with coordinates (x, y)

### OS-Level Click (Undetectable)

```bash
curl -X POST http://localhost:8081 \
  -H 'Content-Type: application/json' \
  -d '{"action": "system_click", "x": 400, "y": 250}'
```

### OS-Level Type (Undetectable)

```bash
curl -X POST http://localhost:8081 \
  -H 'Content-Type: application/json' \
  -d '{"action": "system_type", "text": "search query"}'
```

### Wait for Element

```bash
curl -X POST http://localhost:8081 \
  -H 'Content-Type: application/json' \
  -d '{"action": "wait_for_element", "selector": "#results", "timeout": 10}'
```

### Screenshot

```bash
curl http://localhost:8081/screenshot/browser?whLargest=512 -o screenshot.png
```

## VNC Access

**Live view in browser:**
```
http://localhost:5901/
```

Watch the browser in real-time!

## Use Cases

### 1. Bypass 403/Rate-Limits

```bash
# Navigate to protected site
curl -X POST http://localhost:8081 \
  -d '{"action": "goto", "url": "https://www.finanzen.net/zertifikate/..."}'

# Get content
curl -X POST http://localhost:8081 \
  -d '{"action": "get_text"}'
```

### 2. Persistent Login

```bash
# Login once
curl -X POST http://localhost:8081 \
  -d '{"action": "goto", "url": "https://example.com/login"}'

curl -X POST http://localhost:8081 \
  -d '{"action": "system_click", "x": 300, "y": 200}'

curl -X POST http://localhost:8081 \
  -d '{"action": "system_type", "text": "user@example.com"}'

# Cookies persist in /userdata → Already logged in next time!
```

### 3. Scrape Derivatives

```bash
curl -X POST http://localhost:8081 \
  -d '{"action": "goto", "url": "https://www.hsbc-zertifikate.de/produkte/suche?search=VLO"}'

curl -X POST http://localhost:8081 \
  -d '{"action": "wait_for_element", "selector": "#results"}'

curl -X POST http://localhost:8081 \
  -d '{"action": "get_text"}'
```

## Container Management

### Status

```bash
docker ps --filter "name=stealth-browser"
```

### Logs

```bash
docker logs stealth-browser
```

### Restart

```bash
docker restart stealth-browser
```

### Stop/Remove

```bash
docker stop stealth-browser
docker rm stealth-browser
```

## Persistent Data

**Profile directory:**
```
~/.openclaw/stealth-browser-profile/
```

Contains:
- Cookies (persist across restarts)
- LocalStorage
- Browser sessions
- Fingerprints

**Fresh start:**
```bash
rm -rf ~/.openclaw/stealth-browser-profile/*
docker restart stealth-browser
```

## Security

| Feature | Status |
|---------|--------|
| Ports localhost only | ✅ |
| Read-only filesystem | ✅ |
| No capabilities | ✅ |
| No new privileges | ✅ |
| API authentication | ❌ (never expose!) |

**WARNING:** API has NO authentication. Never expose ports publicly!

## Troubleshooting

| Error | Solution |
|-------|----------|
| Connection refused | `docker ps` check, wait 30-60s on first run |
| Slow browser | Increase tmpfs: `size=1g` |
| 403 still occurring | Try different profile, clear cookies |

## Files

- `scripts/stealth-api.sh` - Wrapper script for API calls
- `references/security.md` - Security configuration details
