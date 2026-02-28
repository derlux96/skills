# Security Configuration - Stealth Browser

## Container Security

| Feature | Setting | Purpose |
|---------|---------|---------|
| Ports | `127.0.0.1:8081:8080` | Localhost only |
| Filesystem | `--read-only` | Immutable container |
| tmpfs | `/tmp:rw,noexec,nosuid,size=512m` | Secure temp |
| Capabilities | `--cap-drop=ALL` | No Linux caps |
| Privileges | `--security-opt=no-new-privileges` | No escalation |

## Docker Run Command

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

## API Security

**WARNING:** API has NO authentication!

### Safe Usage

- ✅ Only bind to localhost (`127.0.0.1`)
- ✅ Never expose ports publicly
- ✅ Use behind reverse proxy with auth (production)
- ✅ Firewall block external access

### Unsafe Usage

- ❌ Binding to `0.0.0.0` (all interfaces)
- ❌ Port forwarding from router
- ❌ Exposing via ngrok/tunnel

## User Data

**Profile path:** `~/.openclaw/stealth-browser-profile/`

### Contains

- Browser cookies
- LocalStorage
- Session data
- Fingerprints

### Isolation

Each agent/user should have separate profile:

```bash
# Agent-specific profile
-v ~/.openclaw/agents/tradepeter/browser-profile:/userdata

# Shared profile
-v ~/.openclaw/stealth-browser-profile:/userdata
```

## Network Security

| Port | Purpose | Exposure |
|------|---------|----------|
| 8081 | REST API | Localhost only |
| 5901 | VNC (noVNC) | Localhost only |

## Resource Limits

Optional limits for production:

```bash
--memory=2g \
--cpus=2 \
--pids-limit=256
```

## Image

- **Repository:** `psyb0t/stealthy-auto-browse`
- **Base:** Ubuntu + Chromium
- **Features:** Playwright, OS-level input, noVNC

## Audit

Verify security:

```bash
# Check port bindings
docker port stealth-browser

# Should show:
# 8080/tcp -> 127.0.0.1:8081
# 5900/tcp -> 127.0.0.1:5901

# Check capabilities
docker inspect stealth-browser | jq '.[0].HostConfig.CapDrop'
# Should show: ["ALL"]

# Check read-only
docker inspect stealth-browser | jq '.[0].HostConfig.ReadonlyRootfs'
# Should show: true
```
