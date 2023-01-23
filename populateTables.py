import json
import pymysql

# Connect to the MySQL database
connection = pymysql.connect(host="localhost", user="root", password="example", db="API_CHU_CAEN", port=3307)
cursor = connection.cursor()

# Read the JSON file
with open('data.json') as f:
    data = json.load(f)

# Insert the data into the MySQL database

for item in data["employé.e informatique"]:
    for key, value in item.items() :
        sql = "INSERT INTO employe (nom, prenom, age, profession) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (value[0], value[1], value[2], value[3]))
    


for item in data["materiel"]:
    for key, value in item.items() :
        sql = "INSERT INTO materiel (nom_du_produit, dimension, etat) VALUES (%s, %s, %s)"
        cursor.execute(sql, (value[0], value[1], value[2]))


# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
