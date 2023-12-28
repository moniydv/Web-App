# Web-Appointments
web application - handles appointments


TECHNOLOGIES USED: 

PERL
JSON
SQL (can be any type of SQL)
JQUERY
HTML


PROJECT REQUIREMENTS : 


This web application handles appointments.
The appointments will be stored in a SQL database with at least 1 table. 
We recommend that one of the tables contains 2 columns: 
(1) a datetime column which records the appointment's time and (2) a description column.

The back-end will be a PERL CGI script which handles requests
from the browser.  There are 3 types of requests which the PERL script
will handle:

1. If no CGI parameters are passed to the back-end PERL script then the
   PERL script renders the HTML document which contains the front-end.

2. If any of the AJAX parameters are provided, then this request is
   considered to be an AJAX call and the PERL script renders the results
   as a JSON document.

3. If this is a form submission, the PERL script will add a NEW
   appointment to the SQL database using the values from the HTML form.
   The PERL script then renders the HTML document which contains the
   front-end just like in #1.

The frontend is a single web page which displays a "NEW" button, an
empty text field with a "SEARCH" button and the bottom of the page will
be an (initially empty) area for displaying the appointments in a table.

	=============================================
	=  +---+
	=  |NEW|
	=  +---+
	=  
	=  +-------------------+  +------+
	=  |                   |  |SEARCH|
	=  +-------------------+  +------+
	=
	=  <appointments table will be here>
	=============================================

The appointments area is initially empty. The document's jQuery DOM
ready function will contain a call to a Javascript
getAppointments() function.

The Javascript getAppointments() function populates the appointments
area (the DOM above). getAppointments() will accept an optional search string.
getAppointments() issues an AJAX 'getAppointments' call to the back-end PERL CGI script,
passing the optional search string. The back-end will reply with a JSON
document containing the matching appointments, and the front-end will use the
resulting JSON object to render the data into the HTML <table> element.  
The resulting HTML is inserted into the DOM so that the <table> appears below the search box.

	==============================================
	=  
	=  +---+
	=  |NEW|
	=  +---+
	=  
	=  +-------------------+  +------+
	=  |                   |  |SEARCH|
	=  +-------------------+  +------+
	=  
	=  +-------+---------+----------------+
	=  | DATE  | TIME    | DESCRIPTION    |
	=  +-------+---------+----------------+
	=  | May 2 | 11:00am | Something      |
	=  | May 2 | 12:00pm | Something else |
	=  | May 4 |  8:00am | Meet foo       |
	=  +-------+---------+----------------+
	=  
	==============================================

If the user enters text into the search text box and hits the SEARCH
button, the appointments area should clear and getAppointments() should
be called with text from the search box.  If the search text box is empty
when the SEARCH button is clicked, then ALL of the appointments should appear.
This should dynamically refresh the Table DOM, and not refresh the entire page.

	==============================================
	=  
	=  +---+
	=  |NEW|
	=  +---+
	=  
	=  +-------------------+  +------+
	=  | Something         |  |SEARCH|
	=  +-------------------+  +------+
	=  
	=  +-------+---------+----------------+
	=  | DATE  | TIME    | DESCRIPTION    |
	=  +-------+---------+----------------+
	=  | May 2 | 11:00am | Something      |
	=  | May 2 | 12:00pm | Something else |
	=  +-------+---------+----------------+
	=  <notice only the rows containing "Something" appear>
	==============================================

The page should also contain a hidden form which contains fields for
adding a new appointment to the database.  Pressing the "NEW" button
changes the "NEW" button to "ADD" and shows the hidden form.

The hidden form should include a "CANCEL" button.  If the "CANCEL" button is
pressed, the form is hidden and the "ADD" button becomes "NEW" again.

	==============================================
	=  
	=  +---+ +------+
	=  |ADD| |CANCEL|
	=  +---+ +------+
	=  
	=       +--------------------+
	=  DATE |                    |
	=       +--------------------+
	=       +--------------------+
	=  TIME |                    |
	=       +--------------------+
	=       +--------------------+
	=  DESC |                    |
	=       +--------------------+ 
	=  
	=  +-------------------+  +------+
	=  |                   |  |SEARCH|
	=  +-------------------+  +------+
	=  
	=  +-------+---------+----------------+
	=  | DATE  | TIME    | DESCRIPTION    |
	=  +-------+---------+----------------+
	=  | May 2 | 11:00am | Something      |
	=  | May 2 | 12:00pm | Something else |
	=  | May 4 |  8:00am | Meet foo       |
	=  +-------+---------+----------------+
	=  
	==============================================

When data is entered into the form and the "ADD" button is pressed, the
form should be submitted to the back-end.  Submitting the form also
reloads the entire web page.  (In other words, the form should be
submitted using normal HTML form semantics.  Don't need to submit the
form as an AJAX call.)

BEFORE RUNNING THE SOLUTION, READ BELOW INSTRUCTIONS:

- The hash bang line in file : index.cgi should be changed to #!/usr/bin/perl OR #!perl/bin/perl based on the location of perl. For Window OS #!C:/perl64/bin/perl has been used in index.cgi
- The date format acceptable on appointment is MM/DD/YYYY. Though regex has been added for MM/DD/YYYY, MM-DD-YYYY, MM.DD.YYYY , but datepicker supports only MM/DD/YYYY format.
- The time format acceptable on appointment is HH::MM (24-hour format) or hh::mm am/pm (12-hour format).
- Search is applicable on Description column of the table (as shown in example of Coding Excercise) only. The search can be enhanced to date and time, by changing date and time format shown in table to DB date-time format.
- When there are no matches for search instead of not showing any result, All appointments are shown to user and a message string displays "No match(es) found".
