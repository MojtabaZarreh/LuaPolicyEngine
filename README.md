# LuaPolicyEngine
This project demonstrates a powerful architectural pattern: embedding a lightweight scripting engine (Lua) inside a robust backend framework (Django) to handle complex, changing authorization logic without restarting the server.


## Why This Architecture? (The Concept of Embedding)
In traditional web development, permissions are hardcoded in Python:
```python
# The Old Way (Hardcoded)
if user.role == 'admin' and document.created_at > yesterday:
    return True
```
If business rules change ("Allow editors to delete documents on weekends"), you have to rewrite code, run tests, and redeploy the server.

The Solution: Embedding Lua By using Lupa (a Python wrapper for LuaJIT), we embed the Lua runtime directly into our Python process. This allows us to:

Decouple Logic: Move business rules out of the codebase and into the database.

Hot-Reloading: Change policies in real-time by updating a database record. No redeployments required.

Sandboxing: Execute untrusted logic safely within a controlled environment.


## Key Features 🚀
⚡ Lua Runtime Integration: Uses lupa to execute high-performance Lua scripts within Python.

🥷 Django Ninja Support: Seamless integration with modern async-ready APIs.

🧠 Smart Caching: Implements intelligent caching (via Redis/Memcached) to prevent re-evaluating Lua scripts for every request (hashed by user + document + time).

🔍 Attribute Injection: Automatically injects User and Document attributes into the Lua context.
