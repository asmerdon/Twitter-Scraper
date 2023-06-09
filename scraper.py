import csv

from facebook_scraper import get_profile

data = get_profile("alex.smerdon.9")

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for key, value in data.items():
        writer.writerow([key, value])