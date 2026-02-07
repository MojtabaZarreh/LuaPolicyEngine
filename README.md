# LuaPolicyEngine
This project demonstrates a powerful architectural pattern: embedding a lightweight scripting engine (Lua) inside a robust backend framework (Django) to handle complex, changing authorization logic without restarting the server.


## Why This Architecture? (The Concept of Embedding)
In traditional web development, permissions are hardcoded in Python:
```Python
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


## 🛠️ How It Works
Request Interception: The @policy_check decorator intercepts the request.

Context Building: Python gathers necessary data (User role, Document stats, Time).

Cache Lookup: Checks if a decision was already made for this specific context recently.

Lua Execution: If not cached, the can_execute function (stored in DB) is run by the embedded Lua engine.

Decision: The boolean result determines access.

## 💻 Usage Example
### 1. The Policy (Stored in Database)
Instead of Python code, you save this Lua script in your Policy model:
```Lua
-- Policy Name: delete_document_policy
function can_execute(user, doc, hour, minute)
    -- Rule 1: Admins can always delete
    if user.role == "admin" then
        return true
    end

    -- Rule 2: Guests are never allowed
    if user.role == "guest" then
        return false
    end

    -- Rule 3: Editors can delete if the doc is small (< 1KB) 
    -- and it's during working hours (9 to 17)
    if user.role == "editor" and doc.content_length < 1024 then
        if hour >= 9 and hour <= 17 then
            return true
        end
    end

    return false
end
```
### 2. The Python Implementation
Simply decorate your API endpoint with the policy name.
```python
from ninja import NinjaAPI
from .policy import policy_check

api = NinjaAPI()

@api.delete("/documents/{document_id}")
@policy_check("delete_document_policy") 
def delete_document(request, document_id: int):
    # This code only runs if Lua returns true!
    return {"success": True, "message": "Document deleted."}
```

## ⚠️ Notes on Security
While Lua is safer than eval(), running dynamic code always carries risk.

Ensure only trusted admins can write to the Policy table.

The current implementation uses a basic environment. For production, consider restricting the Lua globals (e.g., disabling os or io libraries inside Lua).
