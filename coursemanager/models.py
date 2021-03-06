from django.db import models
from coursemanager.utils.datefunctions import get_week, get_month

ATTENDANCESTATUS = (
                    ("A","ABSENT"),
                    ("B", "BOOKED"),
                    ("C", "CANCELLED"),
                    ("D", "ATTENDED"),)

PRESENTATIONSTATUS = (("P","PROVISIONAL"), 
                      ("O","OPEN"),
                      ("C","CLOSED"),
                      ("X","CANCELLED"),
                      ("D","DELIVERED"),
                      ("-","COMPLETED")) 


class Trainer(models.Model):
    emailaddress = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    extension = models.CharField(max_length=15)

    @property
    def trd_week(self):
        period = get_week()
        qs = Presentation.objects.select_related('trainer').filter(
            trainer = self,
            startdate__gte = period[0],
            startdate__lte = period[1]
        )
        d = sum([q.course.duration for q in qs])
        return d

    @property
    def trd_month(self):
        period = get_month()
        qs = Presentation.objects.select_related('trainer').filter(
            trainer=self,
            startdate__gte=period[0],
            startdate__lte=period[1]
        )
        d = sum([q.course.duration for q in qs])
        return d

    @property
    def ded_week(self):
        period = get_week()
        qs = Presentation.objects.select_related('trainer').filter(
            trainer=self,
            startdate__gte=period[0],
            startdate__lte=period[1]
        )

        d = sum([q.num_attendees() * q.course.duration for q in qs])
        return d

    @property
    def ded_month(self):
        period = get_month()
        qs = Presentation.objects.select_related('trainer').filter(
            trainer=self,
            startdate__gte=period[0],
            startdate__lte=period[1]
        )

        d = sum([q.num_attendees() * q.course.duration for q in qs])
        return d

    def __unicode__(self):
        return u'%s' % self.emailaddress

    def __str__(self):
        return self.emailaddress


class Venue(models.Model):
    room = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    maxdelegates = models.IntegerField()
    notes = models.TextField()

    def __unicode__(self):
        return u'%s' % self.room

    def __str__(self):
        return self.room


class Course(models.Model):
    title = models.CharField(max_length=125, unique=True)
    duration = models.FloatField(default='1', blank=True, null=True)
    cost = models.FloatField(null=True, blank=True, default='0.00')
    min_attendees=models.IntegerField(default=3)
    max_attendees=models.IntegerField(default=10)

    def __unicode__(self):
        return u'%s' % self.title

    def __str__(self):
        return self.title


class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    title = models.CharField(max_length=125)
    description = models.CharField(max_length=512, null=True, blank=True)
    reference = models.URLField()

    def __unicode__(self):
        return u'%s' % self.title


class Presentation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    startdate = models.DateField()
    starttime = models.TimeField()
    status = models.CharField(max_length=1, choices=PRESENTATIONSTATUS, default='P')
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT)

    def __unicode__(self):
        return u'%s:%s' % (self.course, self.startdate)

    def __str__(self):
        return u'%s:%s' % (self.course, self.startdate)

    def num_attendees(self):
        return Attendee.objects.filter(presentation=self.id).count()
    
    def attendee_check(self):
        if self.num_attendees() < self.course.min_attendees:
            return "<font color=red>Undersubscribed</font>"
        elif self.num_attendees() > self.course.max_attendees:
            return "Oversubscribed"
        else:
            return "<font color=green>Ok</font>"


class Attendee(models.Model):
    presentation = models.ForeignKey(Presentation, on_delete=models.PROTECT)
    emailaddress = models.EmailField()
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    extension = models.CharField(max_length=15)
    notes = models.TextField()
    attendancestatus = models.CharField(max_length=1, choices=ATTENDANCESTATUS, default='B', verbose_name='status')

    def __unicode__(self):
        return u'%s' % self.emailaddress

    def __str__(self):
        return u'%s' % self.emailaddress


class CostCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=125)

    def __unicode__(self):
        return u'%s' % self.code


class Environment(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField()
    reference = models.URLField()

    def __unicode__(self):
        return u'%s' % self.name


class Report(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=80)
    sortorder=models.IntegerField(default=1)
    view = models.CharField(max_length=40)


class ReportParameters_01(models.Model):
    datefrom = models.DateField()
    dateto = models.DateField()