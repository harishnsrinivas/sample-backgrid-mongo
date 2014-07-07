import collections

from django.db import models
from django.utils import timezone

from jsonfield.fields import JSONField


# Create your models here.

CONTACT_INFO_TYPES = (
    ('Phone', 'Phone'),
    ('Fax', 'Fax'),
    ('Voicemail', 'Voicemail'),
    ('Conference','Conference'),
    ('DonotPick','DonotPick'),
    ('Receptionist','Receptionist')
)

class callrecord(models.Model):
    def __unicode__(self):
        return "%s-%s" % (self.user_plan, self.callerph)

    class Meta:
        app_label = 'SuperReceptionist'

    #sound = models.ForeignKey(superreceptionist)
    user_plan_id = models.IntegerField()
    callerph = models.CharField(max_length=256,default=0)
    sr_number = models.CharField(max_length=100,null=False,blank=False)
    callid = models.CharField(max_length=256,default="dummy-dummy")
    start_time = models.DateTimeField(default=timezone.now())
    voiceid = models.CharField(max_length=256, default="dummy-dummy")
    duration = models.IntegerField(default=0)
    billed_pulses = models.IntegerField(default=0)
    destination = models.CharField(max_length=128)
    ftype = models.CharField(max_length=64, default="undef", choices=CONTACT_INFO_TYPES)
    filepath = models.FileField(max_length=256,upload_to='voicemail/%Y/%m/%d', null= True,blank=True, default=None)
    extension = models.IntegerField(null=True,default = None)
    ruleid = models.IntegerField(null=True,default = None)
    is_outgoing = models.BooleanField(default=False)
    coins_deducted = models.IntegerField(default=0)

class callrecordpreference(models.Model):

    class Meta:
        app_label = 'backgridtest'

    preference = JSONField()

