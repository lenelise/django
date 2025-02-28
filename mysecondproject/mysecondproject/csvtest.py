import csv

datalist = [
    {
        "name": "Lene-Lise", 
        "age": 34
    },  
    {
        "name": "Elisabeth",
        "age": 33
    }
]

for data in datalist: 
    name = data.get('name')
    age = data.get('age')
    print(name, age)

with open('userexport.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(datalist)

