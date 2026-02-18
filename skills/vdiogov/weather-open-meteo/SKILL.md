### Mitigation Steps

1. **Remove the dangerous `curl` calls from the wrapper** and replace them with a pure Go/Node/Python implementation that uses an HTTP client instead of spawning a shell process.

2. **If you must keep `curl`**: 
   * Encode the location using `url.QueryEscape` (or `jq @uri` in bash) before forming the URL.
   * Escape the resulting URL string with `%`-encoding **and** protect it from shell injection with `printf '%q'`.

3. **Avoid using the shell** when constructing URLs.  Directly build the URL string in the language runtime, then call the HTTP client.

4. **Add unit tests** for the location‑encoding logic.

5. **Review** the skill to ensure no other path executes arbitrary shell commands with user data.

---
**Suggested patch** (example in Bash wrapper):
```bash
#!/usr/bin/env bash
set -euo pipefail

# Accept a single argument – the location name
# Encode it safely for URLs
encoded=$(printf '%s' "$1" | jq -sRr @uri)

# Use a pure HTTP client (curl already escaped) – keep the call but safe
url="https://geocoding-api.open-meteo.com/v1/search?name=${encoded}&count=1"
...
```

Make sure the wrapper is marked **not** to use the shell with unsanitized input, or replace entirely with a language that safely builds URLs.

---
**Conclusion**
This mitigates the RCE risk while preserving the skill's functionality.
