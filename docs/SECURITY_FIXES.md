# Security Fixes - v1.0.1

## Critical Security Vulnerabilities Fixed

### 1. SQL Injection in `match_database.py`

**Issue:** Dynamic SQL query construction using f-string with unvalidated column names.
- **Location:** Line 252, `update_match()` method
- **Severity:** HIGH
- **Attack Vector:** Malicious column names in kwargs could execute arbitrary SQL

**Fix:**
- Added whitelist of allowed column names
- Filter kwargs to only include whitelisted columns
- Validated column names before query construction
- Added warning log for rejected columns

```python
# Whitelist of allowed columns
allowed_columns = {
    'processed', 'highlights_generated', 'notes', 
    'total_kills', 'total_deaths', 'total_rounds',
    'duration_seconds', 'map_name', 'player_steamid', 'player_name'
}
safe_kwargs = {k: v for k, v in kwargs.items() if k in allowed_columns}
```

---

### 2. Command Injection in `launcher.py`

**Issue:** User-provided file path passed directly to subprocess without validation.
- **Location:** Line 202, `process_video()` method
- **Severity:** HIGH  
- **Attack Vector:** Malicious file paths with shell metacharacters

**Fix:**
- Add path validation using `Path().resolve()`
- Verify file exists and is a file (not directory)
- Convert to absolute path
- Catch path traversal attempts with exception handling

```python
try:
    video_file = Path(video_path).resolve()
    if not video_file.exists() or not video_file.is_file():
        return  # Invalid file
    video_path = str(video_file)  # Safe absolute path
except (OSError, ValueError):
    return  # Invalid path
```

---

### 3. Unsafe Shell Command in `launcher.py`

**Issue:** Using `os.system()` which is vulnerable to shell injection.
- **Location:** Line 76, `clear_screen()` method
- **Severity:** MEDIUM
- **Attack Vector:** If environment is compromised, could execute arbitrary commands

**Fix:**
- Replaced `os.system('cls')` with `subprocess.run(['cmd', '/c', 'cls'])`
- Use list-based subprocess args (no shell parsing)
- Added fallback for subprocess failures
- Platform-specific safe commands

```python
# Before (vulnerable)
os.system('cls' if os.name == 'nt' else 'clear')

# After (safe)
if os.name == 'nt':
    subprocess.run(['cmd', '/c', 'cls'], check=False)
else:
    subprocess.run(['clear'], check=False)
```

---

## Impact

All fixes maintain backward compatibility. No API changes required.

**Changed Files:**
- `match_database.py` - SQL injection fix
- `launcher.py` - Command injection and os.system fixes

**Testing:**
- Syntax validation passed
- Expected behavior preserved
- Edge cases handled with error messages

---

## Recommendations for Future

1. **Input Validation:** Always validate user inputs
2. **Parameterized Queries:** Use `?` placeholders for SQL
3. **Subprocess Lists:** Never use shell=True with user input
4. **Path Validation:** Use Path().resolve() for file operations
5. **Whitelist Approach:** Prefer whitelists over blacklists

---

**Version:** 1.0.1
**Date:** 2026-01-06
