import argparse
from datetime import datetime
import json
import sys
from xml.dom import minidom

histogram={}
package_counts = {}

parser = argparse.ArgumentParser(description="Extract data from update info xml file")
parser.add_argument('--security', help="filter only security updates", action="store_true")
parser.add_argument('filename')
parser.add_argument('whitelist', help="whitelist json file")

start_year = -1
end_year = -1
total_count = 0

def update_histogram(histogram, start_year, end_year):
  for i in range(start_year, end_year + 1):
    if i not in histogram.keys():
      histogram[i] = {}
      for j in range(1, 13):
        histogram[i][j] = 0
  return histogram

args = parser.parse_args()
filename = args.filename
with open(args.whitelist) as json_file:
  whitelist = json.load(json_file)
filter_security = args.security

xmldoc = minidom.parse(filename)
updates = xmldoc.getElementsByTagName("update")
for update in updates:
  update_id = update.getElementsByTagName("id")[0].firstChild.data
  update_type = update.attributes["type"].value
  if filter_security and update_type != "security":
    continue
  update_severity = update.getElementsByTagName("severity")[0].firstChild.data
  update_date = update.getElementsByTagName("issued")[0].attributes["date"].value
  update_date = datetime.fromtimestamp(float(update_date))
  update_Year = update_date.strftime("%Y")

  if start_year == -1:
    start_year = update_Year
  else:
    if start_year > update_Year:
      start_year = update_Year
  if end_year == -1:
    end_year = update_Year
  else:
    if end_year < update_Year:
      end_year = update_Year

  histogram = update_histogram(histogram, int(start_year), int(end_year))
   
  update_Month = update_date.strftime("%m") 
  packages = update.getElementsByTagName("pkglist")[0].getElementsByTagName("collection")[0].getElementsByTagName("package")
  package_names = []
  for package in packages:
    package_name = package.attributes["name"].value
    if package_name not in whitelist["packages"]:
      continue
    # Filter duplicates. Each package is released for multiple architectures, but we are not insterested on that
    if package_name not in package_names:
      package_names.append(package_name)
      histogram[int(update_Year)][int(update_Month)] += 1
      if package_name not in package_counts.keys():
        package_counts[package_name] = 1
      else:
        package_counts[package_name] += 1
      total_count += 1

n = 0

for key in histogram.keys():
  for key2 in histogram[key].keys():
    if histogram[key][key2] != 0:
      n += 1
    sys.stdout.write(str(key).zfill(4) + " " + str(key2).zfill(2) + " " + str(histogram[key][key2]).zfill(5))
    points = histogram[key][key2] *1000 / total_count
    sys.stdout.write('\x1b[6;30;42m')
    for i in range(int(points)):
      sys.stdout.write(" ")
    sys.stdout.write('\x1b[0m')
    sys.stdout.write("\n")
    sys.stdout.flush()
print("Total: " + str(total_count))
print("Avg: " + str(total_count / n))
sorted_d = sorted(((value, key) for (key,value) in package_counts.items()), reverse=True)
print("Package counts ")
print(sorted_d)
