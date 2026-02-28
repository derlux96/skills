# Security Audit - pyonvista

**Date:** 2026-02-15
**Status:** ✅ SAFE (Code-Level)

## Code Analysis

| Check | Status | Notes |
|-------|--------|-------|
| Malware | ✅ Clean | No malicious code |
| Dependencies | ✅ Minimal | Only aiohttp |
| eval/exec | ✅ None | No dynamic code execution |
| System calls | ✅ None | No shell commands |
| License | ✅ MIT | Open source |

## Legal Status

| Aspect | Status | Notes |
|--------|--------|-------|
| API Access | 🟡 Grauzone | Non-public API |
| ToS Compliance | 🔴 Risk | May violate OnVista ToS |
| Use Case | 🟡 OK | Research/Testing |

## Recommendations

1. **Virtual Environment** - Use isolated environment
2. **Rate Limiting** - Built-in (6s between requests)
3. **Testing Only** - Not for production
4. **403 Errors** - Wait 24h, use fallback
5. **Legal** - User responsibility

## Dependencies

```
pyonvista>=0.1.0
aiohttp>=3.8.0
```

Install:
```bash
pip install pyonvista --break-system-packages
```
