from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

import json
from datetime import datetime

from.models import Checklist, ChecklistItem

# Create your views here.
class GetAllChecklistsView(APIView):
    """
    Retrieve all checklists for a user
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        checklists = []
        for checklist in request.user.checklist_set.order_by('order'):
            checklistJson = checklist_to_json(checklist)
            checklists.append(checklistJson)
        return JsonResponse({'checklists':checklists})

class SaveChecklistOrderView(APIView):
    """
    save order and titles of checklists. Also deletes any missing checklists.
    Data comes in like this:
    {"checklists":[{"pk":1, "title":"winterizing"},{"pk":2, "title":"house"}]}
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = json.loads(request.body)
        checklists = data.get("checklists", [])
        server_checklist_pks = set()
        for checklist in request.user.checklist_set.all():
            server_checklist_pks.add(checklist.pk)
        for i, checkJ in enumerate(checklists):
            checklist = Checklist.objects.get(pk=long(checkJ.get("pk")))
            checklist.title = checkJ.get("title", "")
            checklist.order = i
            checklist.save()
            server_checklist_pks.remove(checklist.pk)
        #delete any checklists that did not come in in the reorder call
        Checklist.objects.filter(pk__in=server_checklist_pks).delete()
        return JsonResponse({'status':'SUCCESS'})

class CreateChecklistView(APIView):
    """
    Create a new checklist or updates a current one if the checklist is synced.
    Request body should be in the format:
    {"pk":1,"title":"test checklist","order":0,"parent":null,"items":[{"text":"test1","checkable":false,"checked":false}]}
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = json.loads(request.body)
        title = data.get("title", "")
        owner = request.user
        if data.get("parent", None):
            parent = long(data["parent"])
        else:
            parent = None
        order = data.get("order", 0)
        if data.get('pk', None) and not data.get('unSynced', True):
            pk = long(data["pk"])
            checklist = Checklist.objects.get(pk=pk)
            checklist.title = title
            checklist.order = order
            checklist.save()
        else:
            checklist = Checklist.objects.create(
                title=title,
                owner=owner,
                parent=parent,
                order=order
            )
        for i, itemJ in enumerate(data.get('items', [])):
            text = itemJ.get('text', "")
            checkable = itemJ['checkable']
            checked = itemJ['checked']
            if itemJ.get('pk', None):
                pk = long(itemJ["pk"])
                item = ChecklistItem.objects.get(pk=pk)
                item.text = text
                item.checkable = checkable
                item.checked = checked
                item.order = i
                item.save()
            else:
                ChecklistItem.objects.create(
                    text=text,
                    checkable=checkable,
                    checked=checked,
                    order=i,
                    checklist=checklist
                )
        checklist.save()
        return JsonResponse({'checklist':checklist_to_json(checklist), 'status':'SUCCESS'})

def checklist_to_json(checklist):
    """
    Creates dict in format:
    {"title":"test checklist","order":0,"parent":null,"items":[{"text":"test1","checkable":false,"checked":false}]}
    """
    checklistJson = {}
    checklistItems = []
    checklistJson['pk'] = checklist.pk
    checklistJson['parent'] = checklist.parent
    if checklist.parent is not None:
        checklist = checklist.parent
    checklistJson['title'] = checklist.title
    checklistJson['order'] = checklist.order
    checklistJson['last_modified'] = long((checklist.last_modified.replace(tzinfo=None) - datetime.utcfromtimestamp(0)).total_seconds()*1000)
    for checklistItem in checklist.checklistitem_set.all().order_by('order'):
        item = {}
        item['pk'] = checklistItem.pk
        item['text'] = checklistItem.text
        item['checkable'] = checklistItem.checkable
        item['checked'] = checklistItem.checked
        item['order'] = checklistItem.order;
        checklistItems.append(item)
    checklistJson['items'] = checklistItems
    return checklistJson
