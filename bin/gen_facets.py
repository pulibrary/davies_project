from csv import DictReader, DictWriter


datafile = "../alb1876.csv"

records = []
with open(datafile, encoding='utf-8') as f:
    reader = DictReader(f)
    for row in reader:
        records.append(row)

libs_by_state = {}
libs_by_type = {}
for record in records:
    if record["State"] not in libs_by_state:
        libs_by_state[record["State"]] = []
    libs_by_state[record["State"]].append(record)

    if record["Type"] not in libs_by_type:
        libs_by_type[record["Type"]] = []
    libs_by_type[record["Type"]].append(record)

    
fieldnames = reader.fieldnames

for state in libs_by_state.keys():
    with open(f"{state}.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rec in libs_by_state[state]:
            writer.writerow(rec)
        
for type in libs_by_type.keys():
    with open(f"{type}.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rec in libs_by_state[state]:
            writer.writerow(rec)
    
