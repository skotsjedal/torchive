# Project Analysis and Suggested Updates

## Current structure
- `torchive/app.py` hosts the Flask routes for archive management (listing downloads, extracting RAR files, copying/moving/deleting outputs, streaming MKV files) and ties into mediainfo helpers. Most handlers interact directly with `localsettings` paths and file utilities.
- `torchive/auth.py` implements HTTP Basic Auth using credentials stored in `localsettings`, wrapping routes with the `requires_auth` decorator.
- Media parsing and lookup logic lives under `torchive/mediainfo` (regex-driven parsing plus IMDB lookups), while `torchive/objectcacher` provides a small caching utility.

## Recommended updates
1. **Migrate to Python 3 and modern Flask patterns.** The codebase uses Python 2 syntax (e.g., `except Exception, e` and bare `print` statements) and imports that are deprecated in modern Flask releases. Updating the runtime would remove EOL dependencies, enable type hints, and allow the app to run on maintained interpreter versions.
2. **Tighten error handling and logging.** Several routes swallow exceptions with generic `except:` blocks or return minimal JSON errors. Converting these to explicit exceptions, logging stack traces, and normalizing error responses will make operational issues easier to diagnose.
3. **Improve authentication and configuration hygiene.** Credentials are read directly from `localsettings.py` and compared in plain text. Consider loading secrets from environment variables, hashing stored values, and enforcing HTTPS to avoid leaking credentials via Basic Auth.
4. **Harden file and streaming operations.** Routes like `copy`, `move`, and `delete` accept user-controlled paths and operate on the filesystem without validation. Adding path normalization, allowed-root checks, and size limits—plus using `send_file` or chunked responses for streaming—would reduce the risk of path traversal and runaway resource usage.
5. **Add automated tests and dependency pinning.** There are no test modules or dependency manifests beyond the README bullet list. Introducing `requirements.txt/poetry.lock` and basic request-level tests (happy-path and failure cases) will document dependencies, detect regressions, and accelerate future refactors.
