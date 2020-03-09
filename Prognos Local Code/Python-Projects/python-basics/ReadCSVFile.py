import csv
from collections import defaultdict
my_dict = defaultdict(list)

with open('tableInCSV.csv','r') as infile:
      reader = csv.reader(infile)
      with open('new.csv','w') as outfile:
          writer = csv.writer(outfile)
          mydict = {rows[0]:rows[1] for rows in reader}

      #
      # for line in csv_reader:
      #     for key, value in line.items():
      #         print(my_dict[key].append(value))
