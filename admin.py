from django.contrib import admin

from .models import Checklist, ChecklistItem, ChecklistEntry

class ChecklistItemInline(admin.StackedInline):
    model = ChecklistItem
    extra = 3

class ChecklistAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemInline]

# Register your models here.
admin.site.register(Checklist, ChecklistAdmin)
