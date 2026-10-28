import os, base64, hashlib, subprocess, sys

TOKEN_DIR = "/root/.garminconnect"
TOKEN_FILE = os.path.join(TOKEN_DIR, "garmin_tokens.json")
# Remembers which GARMINTOKENS_BASE64 value was last written to the volume
MARKER_FILE = os.path.join(TOKEN_DIR, ".seeded_token_hash")

print("=== start.py is running ===", flush=True)

b64 = os.environ.get("GARMINTOKENS_BASE64", "")
print(f"GARMINTOKENS_BASE64 length: {len(b64)}", flush=True)

cleaned = "".join(b64.split())
env_hash = hashlib.sha256(cleaned.encode()).hexdigest() if cleaned else ""

os.makedirs(TOKEN_DIR, exist_ok=True)

old_hash = ""
if os.path.exists(MARKER_FILE):
    with open(MARKER_FILE) as f:
        old_hash = f.read().strip()

token_exists = os.path.exists(TOKEN_FILE)

if cleaned and (not token_exists or env_hash != old_hash):
    # New token pasted into Railway (or no token on the volume yet): write it
    cleaned += "=" * (-len(cleaned) % 4)
    try:
        decoded = base64.b64decode(cleaned)
        print(f"Decoded successfully: {len(decoded)} bytes", flush=True)
    except Exception as e:
        print(f"DECODE FAILED: {e}", flush=True)
        sys.exit(1)
    with open(TOKEN_FILE, "wb") as f:
        f.write(decoded)
    with open(MARKER_FILE, "w") as f:
        f.write(env_hash)
    print("Wrote token from GARMINTOKENS_BASE64 to the volume", flush=True)
elif token_exists:
    # Same variable as last time: keep the (possibly refreshed) token on the volume
    print("Keeping existing token on the volume", flush=True)
else:
    print("ERROR: no token on the volume and GARMINTOKENS_BASE64 is empty!", flush=True)
    sys.exit(1)

print("Files now in /root/.garminconnect:", os.listdir(TOKEN_DIR), flush=True)
print("=== launching garmin-mcp ===", flush=True)
result = subprocess.run(["garmin-mcp"])
# Pass the exit code on, so Railway can see a crash and restart the service
sys.exit(result.returncode)
