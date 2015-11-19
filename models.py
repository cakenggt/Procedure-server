from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Checklist(models.Model):
    """
    Holds checklist items and checklist entries. Can have a parent,
    in which case none of the data in the child checklist is valid,
    but is instead scraped from the parent. The child is not updated
    when this happens.
    """
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    parent = models.ForeignKey('Checklist', null=True, blank=True)
    owner = models.ForeignKey(User)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

class ChecklistItem(models.Model):
    """
    Item in a checklist. Can be a header or a checklist
    entry. Checkable is whether or not it is an entry.
    Checked is whether or not the entry is checked. Headers
    cannot be checked, so only display a checked item if
    checked and checkable are true.
    """
    text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    checklist = models.ForeignKey(Checklist)
    checkable = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text

    def clean(self):
        if not self.checkable:
            self.checked = False
