import os, base64, subprocess

b64 = os.environ.get("GARMINTOKENS_BASE64", "")
cleaned = "".join(b64.split())
cleaned += "=" * (-len(cleaned) % 4)

os.makedirs("/root/.garminconnect", exist_ok=True)
with open("/root/.garminconnect/garmin_tokens.json", "wb") as f:
    f.write(base64.b64decode(cleaned))

subprocess.run(["garmin-mcp"])
