from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from mycalendar.models import User, Calendar, Event, BelongsTo
from django.urls import reverse
import datetime
from django.utils import timezone


# Create your views here.

def mainindex(request):
        context = { 'user_list': User.objects.all() }
        return render(request, 'mycalendar/index.html', context)

def userindex(request, user_id):
        context = { 'user': User.objects.get(pk=user_id), 'calendar_list': User.objects.get(pk=user_id).calendar_set.all() }
        return render(request, 'mycalendar/userindex.html', context)

def eventindex(request, event_id):
        event = Event.objects.get(pk=event_id)
        statuses = [(c.title, BelongsTo.Status(BelongsTo.objects.get(event=event, calendar=c).status)) for c in event.calendars.all()]
        context = {'event': event, 'statuses': statuses}
        return render(request, 'mycalendar/eventindex.html', context)

def calendarindex(request, calendar_id):
        context = { 'calendar_id': calendar_id, 'event_list': Calendar.objects.get(pk=calendar_id).event_set.all() }
        return render(request, 'mycalendar/calendarindex.html', context)

def createevent(request, user_id):
        context = { 'user': User.objects.get(pk=user_id), 'calendar_list': Calendar.objects.all() }
        return render(request, 'mycalendar/createevent.html', context)

def submitcreateevent(request, user_id):
        chosen_calendars = [c for c in Calendar.objects.all() if request.POST["answer{}".format(c.id)] == "true"]
        e = Event(title=request.POST["title"], start_time=request.POST["start_time"], end_time=request.POST["end_time"], created_by = User.objects.get(pk=user_id))
        e.save()
        for c in chosen_calendars:
            bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.WAITING_RESPONSE)
            bt.save()
        return HttpResponseRedirect(reverse('createdevent', args=(user_id,e.id,)))

def createdevent(request, user_id, event_id):
    return eventindex(request, event_id)

def waiting(request, user_id, calendar_id):
        context = {}
        return render(request, 'mycalendar/waiting.html', context)

# Here we will compute some statistics about the data in the database
# Specifically: for each calendar, we will compute the number of events in different status, and a total as a 6-tuple
# The tuple fields are: (calendar title, number of waiting response events, number of accepted events, number of declined events, number of tentative events, total)
# ('John\'s Work Calendar, 1, 4, 3, 4, 10)
def summary(request):
    summary_tuples = [('Sample Calendar', 1, 4, 3, 4, 10)]
    context = {'summary_tuples': summary_tuples}
    return render(request, 'mycalendar/summary.html', context)
