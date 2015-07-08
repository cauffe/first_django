#!/usr/bin/env python
import csv
import os
import sys

sys.path.append("..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_states.settings")

from main.models import State

states = State.objects.all()


csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "states.csv")

csv_file = open(csv_file_path, 'r')

reader = csv.DictReader(csv_file)

for row in reader:
    new_state, created = State.objects.get_or_create(name = row['state'])

    print created

    new_state.abbreviation = row['abbrev']
    new_state.name = row['state']
    new_state.capital = row['capital']
    new_state.latitude = row['latitude']
    new_state.longitude = row['longitude']
    new_state.capital_population = row['population']
    
    new_state.save()

csv_file.close()
