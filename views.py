from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from.models import Checklist, ChecklistItem

# Create your views here.
class GetAllChecklistsView(APIView):
    """
    Authentication is needed for this methods
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        checklists = []
        for checklist in Checklist.objects.filter(owner=request.user.id):
            checklistJson = {}
            checklistItems = []
            checklistJson['title'] = checklist.title
            if checklist.parent is not None:
                checklist = checklist.parent
            for checklistItem in checklist.checklistitem_set.all().order_by('order'):
                item = {}
                item['text'] = checklistItem.text
                item['checkable'] = checklistItem.checkable
                item['checked'] = checklistItem.checked
                checklistItems.append(item)
            checklistJson['items'] = checklistItems
            checklists.append(checklistJson)
        return JsonResponse({'checklists':checklists})
