from lupa import LuaRuntime
from functools import wraps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Policy, Document
from django.utils import timezone
from django.core.cache import cache
import hashlib
import json

lua = LuaRuntime(unpack_returned_tuples=True)

def policy_check(policy_name):
    def decorator(func):
        @wraps(func)
        def wrapper(request, document_id, *args, **kwargs):
            user_role = getattr(request.user, "role", "guest")
            user_info = {
                "role": user_role,
                "username": getattr(request.user, "username", "anonymous"),
            }

            try:
                policy = Policy.objects.get(name=policy_name)
            except Policy.DoesNotExist:
                return JsonResponse({"success": False, "message": "Policy not found."}, status=400)

            try:
                document = get_object_or_404(Document, id=document_id)
                now = timezone.now()

                record_data = {
                    "id": document.id,
                    "title": document.title,
                    "content_length": len(document.content),
                    "created_days_ago": (now - document.created_at).days if hasattr(document, 'created_at') else 0,
                }

                cache_key_data = {
                    "user": user_info,
                    "document": record_data,
                    "hour": now.hour,
                    "minute": now.minute,
                }
                cache_key = "policy_cache_" + hashlib.md5(json.dumps(cache_key_data, sort_keys=True).encode()).hexdigest()

                cached_result = cache.get(cache_key)
                if cached_result is not None:
                    allowed = cached_result
                else:
                    lua.execute(policy.lua_code)
                    can_execute = lua.eval("can_execute")

                    lua_user = lua.table_from(user_info)
                    lua_record = lua.table_from(record_data)

                    allowed = can_execute(lua_user, lua_record, now.hour, now.minute)

                    cache.set(cache_key, allowed, timeout=120)

                if not allowed:
                    return JsonResponse({"success": False, "message": "Access denied by policy."}, status=403)

            except Exception as e:
                return JsonResponse({"success": False, "message": f"Lua execution error: {str(e)}"}, status=500)

            return func(request, document_id, *args, **kwargs)
        return wrapper
    return decorator
