echo "Removing existing files"
rm calendarsite/mycalendar/views.py calendarsite/mycalendar/urls.py calendarsite/mycalendar/templates/mycalendar/eventindex.html calendarsite/mycalendar/templates/mycalendar/calendarindex.html calendarsite/mycalendar/templates/mycalendar/waiting.html calendarsite/mycalendar/templates/mycalendar/summary.html

echo "Copying student files"
for i in grading-part1/$1/grading_files/*.py
do
	cp -i $i calendarsite/mycalendar/
done

for i in grading-part1/$1/grading_files/*.html
do
	cp -i $i calendarsite/mycalendar/templates/mycalendar/
done
