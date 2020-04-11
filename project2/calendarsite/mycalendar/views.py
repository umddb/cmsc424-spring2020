from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from mycalendar.models import User, Calendar, Event, BelongsTo
from django.urls import reverse
import datetime
import operator
from django.utils import timezone


# Create your views here.

def mainindex(request):
        context = { 'user_list': User.objects.all() }
        return render(request, 'mycalendar/index.html', context)

def userindex(request, user_id):
        print(User.objects.get(pk=user_id).calendar_set)
        context = { 'calendar_list': User.objects.get(pk=user_id).calendar_set.all() }
        return render(request, 'mycalendar/userindex.html', context)

def eventindex(request, event_id):
        event = Event.objects.get(pk=event_id)
        statuses = [(c.title, BelongsTo.Status(BelongsTo.objects.get(event=event, calendar=c).status)) for c in event.calendars.all()]
        context = {'event': event, 'statuses': statuses}
        return render(request, 'mycalendar/eventindex.html', context)

def calendarindex(request, calendar_id):
        context = {'calendar_id': calendar_id, 'event_list': Calendar.objects.get(
            pk=calendar_id).event_set.all().order_by('start_time')}

        for event in context['event_list']:
                print(type(event.start_time))

        date_list = dict()

        for i in range(0, len(context['event_list'])):
                if context['event_list'][i].start_time.strftime("%B %d, %Y") in date_list:
                        date_list[context['event_list'][i].start_time.strftime("%B %d, %Y")].append(context['event_list'][i])
                else:
                        date_list[context['event_list'][i].start_time.strftime("%B %d, %Y")] = [(context['event_list'][i])]

        context['date_list'] = date_list
        return render(request, 'mycalendar/calendarindex.html', context)

def createevent(request, user_id):
        context = {'user': User.objects.get(pk=user_id), 'calendar_list': Calendar.objects.all()}
        return render(request, 'mycalendar/createevent.html', context)

def modifyevent(request, event_id):
        event = Event.objects.get(pk=event_id)
        context = {'event': event, 'calendar_list': Calendar.objects.all()}
        return render(request, 'mycalendar/modifyevent.html', context)

def submitcreateevent(request, user_id):
        chosen_calendars = [c for c in Calendar.objects.all() if request.POST["answer{}".format(c.id)] == "true"]
        e = Event(title=request.POST["title"], start_time=request.POST["start_time"], end_time=request.POST["end_time"], created_by = User.objects.get(pk=user_id))
        e.save()
        for c in chosen_calendars:
            bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.WAITING_RESPONSE)
            bt.save()
        return HttpResponseRedirect(reverse('createdevent', args=(user_id,e.id,)))

def submitmodifyevent(request, event_id):
        chosen_calendars = [c for c in Calendar.objects.all() if request.POST["answer{}".format(c.id)] == "true"]
        event = Event.objects.get(pk=event_id)
        e = Event(title=request.POST["title"], start_time=request.POST["start_time"], end_time=request.POST["end_time"], created_by = event.created_by)
        Event.objects.get(pk=event_id).delete()
        e.save()
        for c in chosen_calendars:
                bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.WAITING_RESPONSE)
                bt.save()
        return HttpResponseRedirect(reverse('createdevent', args=(1,e.id,)))

def createdevent(request, user_id, event_id):
    return eventindex(request, event_id)

def waiting(request, user_id, calendar_id):
       
        event = Calendar.objects.get(pk=calendar_id).event_set.all()
        
        event_filtered = []

        for e in event:
                c = Calendar.objects.get(pk=calendar_id)
                if BelongsTo.Status(BelongsTo.objects.get(event=e, calendar = c).status) is BelongsTo.Status.WAITING_RESPONSE:
                        event_filtered.append(e)
        context = {'event_list': event_filtered, 'calendar': Calendar.objects.get(pk=calendar_id), 'user': User.objects.get(pk=user_id)}
        return render(request, 'mycalendar/waiting.html', context)

def submitwaiting(request, user_id, calendar_id, event_id):
        e = Event.objects.get(pk=event_id)
        c = Calendar.objects.get(pk=calendar_id)

        BelongsTo.objects.get(event=e, calendar=c).delete()
        
        if request.POST["answer{}".format(c.id)] is "Wait":
                bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.WAITING_RESPONSE)
                bt.save()
        elif request.POST["answer{}".format(c.id)] is "Accept":
                bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.ACCEPTED)
                bt.save()
        elif request.POST["answer{}".format(c.id)] is "Decline":
                bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.DECLINED)
                bt.save()
        elif request.POST["answer{}".format(c.id)] is "Tentative":
                bt = BelongsTo(event=e, calendar=c, status=BelongsTo.Status.TENTATIVE)
                bt.save()

        return HttpResponseRedirect(reverse('waiting', args=(user_id, calendar_id)))

# Here we will compute some statistics about the data in the database
# Specifically: for each calendar, we will compute the number of events in different status, and a total as a 6-tuple
# The tuple fields are: (calendar title, number of waiting response events, number of accepted events, number of declined events, number of tentative events, total)
# ('John\'s Work Calendar, 1, 4, 3, 4, 10)
def summary(request):

        count = dict()
        calendar = Calendar.objects.all()

        for c in calendar:
                event_list = Calendar.objects.get(pk=c.id).event_set.all()
                count[c] = [0,0,0,0,0]
                for e in event_list:
                        if BelongsTo.Status(BelongsTo.objects.get(event=e, calendar=c).status) is BelongsTo.Status.WAITING_RESPONSE:
                                count[c][0] += 1;
                        elif BelongsTo.Status(BelongsTo.objects.get(event=e, calendar=c).status) is BelongsTo.Status.ACCEPTED:
                                count[c][1] += 1;
                        elif BelongsTo.Status(BelongsTo.objects.get(event=e, calendar=c).status) is BelongsTo.Status.DECLINED:
                                count[c][2] += 1;
                        elif BelongsTo.Status(BelongsTo.objects.get(event=e, calendar=c).status) is BelongsTo.Status.TENTATIVE:
                                count[c][3] += 1;
                        count[c][4] += 1;

        summary_tuples = []
        for k,v in count.items():
                tuple = (k, v[0], v[1], v[2], v[3], v[4])
                summary_tuples.append(tuple)

        context = {'summary_tuples': summary_tuples}
        return render(request, 'mycalendar/summary.html', context)

