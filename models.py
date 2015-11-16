from django.db import models

# Create your models here.
class Checklist(models.Model):
    """
    Holds checklist items and checklist entries. Can have a parent,
    in which case none of the data in the child checklist is valid,
    but is instead scraped from the parent. The child is not updated
    when this happens.
    """
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('Checklist')

class ChecklistItem(models.Model):
    """
    Item in a checklist. Can be a header or a checklist
    entry. If the checklistEntry one-to-one recursive field is empty, then it
    is a header.
    """
    text = models.CharField(max_length=200)
    checklist = models.ForeignKey(Checklist)

class ChecklistEntry(models.Model):
    """
    Checkable entry in a checklist. Is a subclass of ChecklistItem and
    has a one-to-one relationship with a ChecklistItem.
    """
    item = models.OneToOneField(ChecklistItem, primary_key=True)
    checked = models.BooleanField(default=False)
