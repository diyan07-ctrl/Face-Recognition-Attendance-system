import csv

def retrieve_classes(user:str, acc_type: str) -> list:
    classes = []
    try:
        with open("../Data/classes.csv", "r") as class_data:
            reader = csv.DictReader(class_data)
            for row in reader:
                if row[acc_type] == user:
                    classes.append(row)
    except Exception as e:
        print(e)
    return classes
