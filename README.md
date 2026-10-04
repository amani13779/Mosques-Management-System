
# Mosques Management System

## Description

Mosques Management System is a Python application designed to manage mosque records using a graphical user interface.

The system allows users to add, display, search, delete, and update mosque information. It also provides a feature to display the mosque location on an interactive map.

## Features

* Add a new mosque
* Display all mosque records
* Search for a mosque by name
* Delete a mosque by ID
* Update the Imam name
* Display mosque location on a map
* Suggest similar mosque names when an exact search is not found

## Mosque Information

Each mosque record contains:

* ID
* Name
* Type
* Address
* Coordinates
* Imam Name

## Technologies Used

* Python
* Tkinter
* SQLite
* Folium
* Webbrowser
* Difflib

## Database

The application uses SQLite to store mosque records.

A database file named `mosques.db` is created automatically when the program runs.

## Map

The application uses Folium to display mosque locations based on latitude and longitude coordinates.

The map is opened in the web browser when the **Display on Map** option is selected.

## How to Run

1. Make sure Python is installed on your computer.
2. Install Folium:

```bash
pip install folium
```

3. Run the Python program:

```bash
python "amani pro3 CS492.py"
```

## Main Operations

### Display All

Displays all mosque records stored in the database.

### Add Entry

Adds a new mosque record after entering all required information.

### Search By Name

Searches for a mosque using its name and provides close matches if an exact match is not found.

### Delete Entry

Deletes a mosque record using its ID.

### Update Entry

Updates the Imam name of an existing mosque.

### Display on Map

Displays the selected mosque location using its coordinates.


Amani Ibrahim Alnafisah
