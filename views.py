from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core import serializers

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
        data = json.loads(request.POST.get('order', '{}'))
        checklists = data.get("checklists", [])
        server_checklist_pks = set()
        for checklist in request.user.checklist_set.all():
            server_checklist_pks.add(checklist.pk)
        for i, checkJ in enumerate(checklists):
            checklist = request.user.checklist_set.get(pk=long(checkJ.get("pk")))
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
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = json.loads(request.POST.get('checklist', '{}'))
        title = data.get("title", "")
        owner = request.user
        if data.get("parent", None):
            parent = Checklist.objects.get(pk=data["parent"])
        else:
            parent = None
        order = data.get("order", 0)
        if data.get('pk', None) and not data.get('unSynced', True):
            pk = data.get('pk', None)
            checklist = owner.checklist_set.get(pk=pk)
            checklist.title = title
            checklist.order = order
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
                if item.checklist.owner != owner:
                    return JsonResponse({'status':'FAILURE'})
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

    Also updates child checklists with their parent's items if they differ.
    """
    checklistJson = {}
    checklistItems = []
    checklistJson['pk'] = checklist.pk
    checklistJson['parent'] = None
    checklistJson['order'] = checklist.order
    checklistJson['last_modified'] = long((checklist.last_modified.replace(tzinfo=None) - datetime.utcfromtimestamp(0)).total_seconds()*1000)
    checklistJson['title'] = checklist.title
    if checklist.parent is not None:
        checklistJson['parent'] = checklist.parent.pk
        parent = checklist.parent
        parent_ci_size = len(parent.checklistitem_set.all())
        child_ci_size = len(checklist.checklistitem_set.all())
        size_difference = parent_ci_size - child_ci_size
        if size_difference > 0:
            # add some items
            for i in xrange(size_difference):
                ChecklistItem.objects.create(
                    text='',
                    checkable=False,
                    checked=False,
                    order=i+parent_ci_size,
                    checklist=checklist
                )
        elif size_difference < 0:
            #remove some items
            for i in xrange(abs(size_difference)):
                checklist.checklistitem_set.all().order_by('order')[parent_ci_size].delete()
        #replace all of the text and checkable attributes when ordering by order, and save each item
        #reorder items so that they go up consecutively
        for i in xrange(parent_ci_size):
            parent_item = parent.checklistitem_set.all().order_by('order')[i]
            child_item = checklist.checklistitem_set.all().order_by('order')[i]
            child_item.order = i
            child_item.text = parent_item.text
            child_item.checkable = parent_item.checkable
            child_item.save()
    for checklistItem in checklist.checklistitem_set.all().order_by('order'):
        item = {}
        item['pk'] = checklistItem.pk
        item['text'] = checklistItem.text
        item['checkable'] = checklistItem.checkable
        item['checked'] = checklistItem.checked
        item['order'] = checklistItem.order
        checklistItems.append(item)
    checklistJson['items'] = checklistItems
    checklist.save()
    return checklistJson

def login_user(request):
    """
    Method called by the login page to log a user in.
    """
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return redirect('procedure:main')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    return render(request, 'procedure/login.html', {'state':state, 'username': username})

@login_required(login_url='/procedure/login/')
def main(request):
    checklists = request.user.checklist_set.all().order_by('order')
    return render(request, 'procedure/main.html', {
        'checklist_list': checklists
    })

def user_logout(request):
    if request.user is not None:
        logout(request)
    return redirect('procedure:login')

@login_required(login_url='/procedure/login/')
def checklist(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if (request.user != checklist.owner):
        return HttpResponseForbidden()
    checklist_items = checklist.checklistitem_set.all().order_by('order')
    checklist_dict = checklist_to_json(checklist)
    checklist_dict['unSynced'] = False
    return render(request, 'procedure/checklist.html', {
        'checklist': checklist,
        'checklist_items': checklist_items,
        'checklist_json': json.dumps(checklist_dict)
    })
