from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Policy(models.Model):
    name = models.CharField(max_length=100)
    lua_code = models.TextField(
        help_text="Lua script defining the policy logic."
    )
    def __str__(self):
        return self.name