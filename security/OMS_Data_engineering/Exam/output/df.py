import csv

with open("output.csv", newline='') as in_file:
    with open("out.csv", 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if any(row):
                writer.writerow(row)