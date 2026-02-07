from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from .models import Document
from .policy import policy_check

api = NinjaAPI()

@api.delete("/documents/{document_id}")
@policy_check("delete_document_policy")
def delete_document(request, document_id: int):
    doc = get_object_or_404(Document, id=document_id)
    doc.delete()
    return {"success": True, "message": "Document deleted successfully."}