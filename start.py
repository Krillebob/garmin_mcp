import os, base64, subprocess, sys

print("=== start.py is running ===", flush=True)

b64 = os.environ.get("GARMINTOKENS_BASE64", "")
print(f"GARMINTOKENS_BASE64 length: {len(b64)}", flush=True)

if not b64:
    print("ERROR: GARMINTOKENS_BASE64 is empty or not set!", flush=True)
    sys.exit(1)

cleaned = "".join(b64.split())
cleaned += "=" * (-len(cleaned) % 4)

try:
    decoded = base64.b64decode(cleaned)
    print(f"Decoded successfully: {len(decoded)} bytes", flush=True)
    print(f"First 100 chars: {decoded[:100]}", flush=True)
except Exception as e:
    print(f"DECODE FAILED: {e}", flush=True)
    sys.exit(1)

os.makedirs("/root/.garminconnect", exist_ok=True)
with open("/root/.garminconnect/garmin_tokens.json", "wb") as f:
    f.write(decoded)

print("Files now in /root/.garminconnect:", os.listdir("/root/.garminconnect"), flush=True)
print("=== launching garmin-mcp ===", flush=True)
subprocess.run(["garmin-mcp"])
