"""
test_setup.py — Run this to verify Disha AI is ready to run.

Run with:  python test_setup.py
"""

import sys
import os
import importlib.util
import shutil

print("=" * 55)
print("  DISHA AI — Setup Verification")
print("=" * 55)
print()

all_ok = True


def check_module(display_name: str, module_name: str) -> bool:
    """Check if a Python module is importable. Returns True if OK."""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        return False


# ── Check 1: Python version ──────────────────────────────────
print("Checking Python version...")
version = sys.version_info
if (3, 10) <= (version.major, version.minor) <= (3, 12):
    print(f"  [OK]  Python {version.major}.{version.minor}.{version.micro}")
else:
    print(f"  [FAIL]  Python {version.major}.{version.minor} — need 3.10, 3.11, or 3.12")
    print("          (3.13+ and pre-release versions are not yet fully supported by ADK)")
    all_ok = False

# ── Check 2-6: Required packages ─────────────────────────────
packages = [
    ("google-adk",      "google.adk"),
    ("google-genai",    "google.genai"),
    ("mcp",             "mcp"),
    ("streamlit",       "streamlit"),
    ("python-dotenv",   "dotenv"),
]

print("\nChecking required packages...")
for display_name, module_name in packages:
    ok = check_module(display_name, module_name)
    print(f"  {'[OK]' if ok else '[FAIL]'}  {display_name}")
    if not ok:
        print(f"          Run:  pip install {display_name}")
        all_ok = False

# ── Check 7: API Key ─────────────────────────────────────────
print("\nChecking Google API Key...")
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
if api_key and len(api_key) > 10:
    masked = api_key[:6] + "..." + api_key[-4:]
    print(f"  [OK]  GOOGLE_API_KEY found ({masked})")
else:
    print("  [FAIL]  GOOGLE_API_KEY not found")
    print("          1. Go to: https://aistudio.google.com/apikey")
    print("          2. Create a free key")
    print("          3. Add to .env file:  GOOGLE_API_KEY=your_key_here")
    all_ok = False

# ── Check 8: npx (Node.js) ───────────────────────────────────
print("\nChecking Node.js / npx (for MCP server)...")
npx = shutil.which("npx")
if npx:
    print(f"  [OK]  npx found at {npx}")
else:
    print("  [FAIL]  npx NOT found")
    print("          Install Node.js from: https://nodejs.org (LTS version)")
    all_ok = False

# ── Check 9: .env file ───────────────────────────────────────
print("\nChecking .env file...")
if os.path.exists(".env"):
    print("  [OK]  .env file exists")
else:
    print("  [WARN]  .env file not found")
    print("          Run:  copy .env.example .env")

# ── Check 10: Memory folder ──────────────────────────────────
print("\nChecking memory store folder...")
from pathlib import Path
mem_path = Path("disha_agent/memory_store")
mem_path.mkdir(parents=True, exist_ok=True)
print(f"  [OK]  {mem_path} ready")

# ── Check 11: Live API test (only if key present) ────────────
if api_key:
    print("\nTesting live connection to Gemini API...")
    try:
        os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")
        from google import genai
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Reply with exactly one word: OK",
        )
        if response and response.text:
            print(f"  [OK]  Gemini API responded: {response.text.strip()[:50]}")
        else:
            print("  [WARN]  Gemini API returned empty response")
    except Exception as e:
        print(f"  [FAIL]  Gemini API call failed: {e}")
        print("          Check your API key is valid and has not expired.")
        all_ok = False

# ── Final result ─────────────────────────────────────────────
print()
print("=" * 55)
if all_ok:
    print("  ALL CHECKS PASSED!")
    print()
    print("  Run the app now:")
    print("    streamlit run app.py")
else:
    print("  SOME CHECKS FAILED")
    print("  Fix the issues above, then run this again.")
print("=" * 55)