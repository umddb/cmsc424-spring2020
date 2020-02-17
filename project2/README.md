## Project 2: Web Development with Python Django, CMSC424, Spring 2020

**This assignment is to be done by yourself, but you are welcome to discuss the assignment with others.**

The goal of this project is to learn how Web Application Frameworks like Python Django (similar to Ruby-on-Rails) work, and
how they interact with the underlying data store. We will be providing you with a skeleton code, and 
describe a set of files that you need to modify. There are several final deliverables for the assignment:

* You have to complete a few files as described below. In the past, students had most trouble with getting things to work, so we have provided skeleton code where all the links etc., work, except that they don't do anything in some cases. You have to implement that functionality by modifying the specified files. In all cases, there is at least one other similar file that you can use as template. The deliverable here is the modified files. **[16/40 pts]**
* We have also provided the Entity-Relationship Diagram corresponding to the implemented functionality, which is quite minimal. You have to extend the E/R diagram so that it can support additional functionality. The deliverable here is the E/R diagram itself. **[12/40 pts]**
* You have to convert the E/R diagram to a relational schema, and write out the `models.py` file for your E/R diagram. You don't need to make it work, just write out the code. Both the reltional schem and the modified `models.py` file should be submitted. **[12/40 pts]**

Submit all the files (E/R diagram as a PDF, the relational schema in a text file, and the modified python files) as a single zip archive.

### Getting Started
As before, we have provided with a VagrantFile, that installs Django and sets up a few port forwards. 
After logging into the virtual machine with `vagrant ssh`, go to: `/vagrant/calendarsite/` and do `python3 manage.py runserver 0.0.0.0:8888`.

This starts a webserver at port 8888, using our application code and data (that is already loaded). Go to: `http://localhost:8888/mycalendar/` for 
the main index page of the web application. See below for more details on the application.

### Introduction to Django
You should walk through the excellent Django tutorial: [Django Tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/) -- we don't cover all of that in the description below since the tutorial does a great job at that. Django is quite popular, and there are quite a few other resources online as well. If you run into an error, searching for the error on Google should lead to some solutions (often on stackoverflow).

The initial web app that we have created is present in `calendarsite/mycalendar` subdirectory (in `/vagrant` on your VM, and `project2` in your host machine).
See below for more details about that app.

Django is a high-level Python Web framework for simplifying creation of complex, database-driven websites. It follows the so-called MVT (Model-View-Template) framework, which is mostly the same as the MVC (Model-View-Controller) framework (used by Ruby Rails framework). These frameworks are usually built around an Object-Relational Mapping (ORM), where the models (defined as Python classes in Django) are transparently mapped to Relations in a backend relational database. 

At a high level, the following things need to be done in order to set up a minimal web application using Django.
* We need to create a set of `models`, which roughly correspond to `entities` in E/R Modeling, and relations in relational databases. In Python code, the models serve as classes of objects, whereas the Django framework takes care of saving any such objects to the database etc. The models are defined in the file `mycalendar/models.py`. You can see the definitions of the models discussed below.
* We need to provide a mapping between URLs and `views`, so that when the web server sees a specific URL, it knows what function to call. See `mycalendar/urls.py` file for these mappings. As an example, the URL `http://localhost:8888/mycalendar/1` will result in a call to `calendarindex` in `views.py`.
* In each of the `views`, we need to collect the appropriate data, and call a `template`. The `calendarindex` view simply finds the Calendar and calls the template `calendarindex`.
* Templates tell the framework what HTML webpages to construct and return to the web browser. Our templates are in `mycalendar/templates/mycalendar` directory (the tutorialdiscusses why this specific directory). The `calendarindex.html` template file has a mix of python commands and HTML, and it creates an HTML page after executing of the Python commands. The resulting HTML is what is returned and displayed on the browser when you call: `http://localhost:8888/mycalendar/1`

**python3 manage.py shell**: This is an important command that allows you to manipulate the data in the database directly (outside of the web application). The file `populate.py` contains the commands used to construct the data in the provided database.

**Database Backend**: Django can work with many database engines, including PostgreSQL (which is recommended for any serious development). Here we are using the `sqlite3` engine, primarily so we can easily provide you with the database (in the `calendarsite/db.sqlite3` file).

**Admin Website**: If you go to `http://localhost:8888/admin` with username `vagrant` and password `vagrant`, you can directly manipulate the objects.

### Application Scenario and the Initial E/R Model
The goal of this web application development project is to build an end-to-end application that has a web frontend, and a database backend.  The application scenario is that of handling an online calendar. Although there are ofcourse quite a few tools out there for this purpose today, we picked this scenario given you are well-familiar with the setting.

As mentioned above, the coding part of this project focuses on a simple set of entities and relationships, as shown in the E/R diagram here. 

![Calendar E/R Diagram](calendar_er.jpg)

The entities here are:
- **Users** who own calendars. A user may own more than one calendar.
- **Calendars** is created and owned by a single user, and contains Events. 
- **Events:**  An event is created by one user, and belongs to one or more calendars. When a user creates a new event, they choose a subset of all the calendars in the system, and `invite` the owners through those calendars. Each of the invited people then choose whether to accept the event or not (including the user who created -- in other words, we allow for the creator of an event to not accept the event).

There are three relationships here:
- **User-to-Calendar**: which records the ownership of calendars. This is recorded implicitly through a ForeignKey constraint.
- **CreatedEvent**: which records who created an event. This is also recorded implicitly through a ForeignKey constraint.
- **BelongsTo**: which records which calendars contain a given event, and the status (Waiting Response, Accepted, Declined, Tentative)

If you open the database using `sqlite3 calendarsite/db.sqlite3`, you can directly see the tables being created. The command `.schema` will show you all the tables that have been created.

The provided application currently has six types of URLs/views/webpages: 
- **mainindex**: Main "index" page, where we simply display a list of users. (example: http://localhost:8888/mycalendar/)
- **userindex**: User "index" page, which shows the list of calendars owned by the user. (example: http://localhost:8888/mycalendar/user/1). This is currently *not implemented*
- **eventindex**: Event "index" page, which shows the details for an event. (example: http://localhost:8888/mycalendar/event/11)
- **calendarindex**: Shows the events in a given calendar, along with the date, time, and status. (example: http://localhost:8888/mycalendar/calendar/1)
- **createevent**: This is the page where a user can create an event by choosing the requisite information, and selecting a group of calendars (example: http://localhost:8888/mycalendar/user/1/create)
- **waiting**: This is the page where a user can see all the events that are in waiting state in one of their calendars, and take action on them (example: http://localhost:8888/mycalendar/waiting/user/1/calendar/1). See below for more details.
- **summary**: This page is intended to show some statistics about the data in the database. See below for the functionality to be implemented (http://localhost:8888/mycalendar/summary)

*Typically you would want to do some authorizations to separate out the different functionality. This is easy to add by having users, and using `sessions`. We will not worry about it for now. Our focus is on designing the E/R model and the schema, and understanding how to use Django.*

### Assignment Part 1: Files to be Modified

All your modifications will be to the `views.py` file, `urls.py` file, or to one of the template files in `mycalendar/templates/mycalendar`. Specifically, the following
pieces need to be fixed. First 4 are 2 pts each, the last two are 4 pts each.

1. Modify `eventindex.html` template file to list the name of the user who created the event.
1. Modify `calendarindex.html` template file so that the `Event Titles` are *clickable*, i.e., they are links which take to the detailed Event page (i.e., to pages like: http://localhost:8888/mycalendar/event/11)
1. Modify `calendarindex.html` template file to show the Events sorted by time, and separated by the days. In other words, there should be separate table for each date in order. 
1. Modify the function `summary` in `views.py` to construct the appropriate summary statistics to be sent to the template file. 
1. Analogous to **createevent**, add a new path: **modifyevent**. If a user were to go to: http://localhost:8888/mycalendar/modifyevent/11, they should be able to modify the details like the start/end time, event name, and who was invited. All `status` should be set to 'WR'. This will require adding a new path to `urls.py`, addition of a new template file `modifyevent.html`, and a new function in `views.py`. Use `createevent` as a starting point -- a lot of the code can be reused.
1. Implement the `waiting` page. Here a user can see all the events that are currently in *WR* state, and can modify the status for any of them, and then press submit to save the changes. The user is not required to set a new status on all of the events that are currently awaiting response. 


### Assignment Part 2: Extend E/R Model

Our E/R model is pretty simplistic. You need to modify it so it allows representing the following types of information.
- A user should be able to set permissions for each of their calendars, by choosing who else (i.e., which other users) can "see" the events in that calendar.
- An event should be allowed to `repeat` on a schedule. Specifically, for a event, we should be able to record a repeat frequency (daily, weekly, weekly on multiple days, monthly, etc). Just like Google calendar, there should be an end date associated with the repeated events. For simplicity, we will assume that a user has the same statuts for all repetitions of an event (unlike say Google Calendar, which allows me to say Yes to an event today, but no to the repeated event next week).
- For each event, a user should be able to record a "priority" number, i.e., how important is that event for them. (This can be used, e.g., for resolving scheduling conflicts). Priority is a numeric rating between 1 and 5 (5 being highest priority). The priority for the same event may be different for different users (e.g., a specific meeting might be high priority for one user, but low priority for another user).
- Add another type of entity: a `Room`. Events can be scheduled in rooms, so we also need to add the appropriate relationship. The attributes of room include the room number, room name (may be null), and capacity.
- Add another type of entity: a `Company` that a person belongs to. If the person tries to create an event that involves non-company users, this information will help us
warn them. Attributes of a company include company name, and address.


Here is a link to the [Google Drawing of the E/R Diagram](https://docs.google.com/drawings/d/1z8ZvOfoRaruk1iJmfivTjazOYLz3N4vF_usgHv7MtHg/edit?usp=sharing) above. You are welcome to copy it and modify it. Submit the final E/R diagram as a PDF file.

### Assignment Part 3: `models.py` for your E/R Model

Modify the `models.py` file according to your new E/R models. You are welcome to try to make it work with the rest of the app, but we only need the models.py file, and the grading will be by inspection, not by running it.
