from utils import connect_to_mongodb


client = connect_to_mongodb()
db = client['datasolutech']
collection = db['collection_test']

patient1 = {
        "Name": "Bobby JacksOn",
        "Age": 30,
        "Gender": "Male",
        "Blood Type": "B-",
        "Medical Condition": "Cancer",
        "Date of Admission": "2024-01-31",
        "Doctor": "Matthew Smith",
        "Hospital": "Sons and Miller",
        "Insurance Provider": "Blue Cross",
        "Billing Amount": 18856.281305978155,
        "Room Number": 328,
        "Admission Type": "Urgent",
        "Discharge Date": "2024-02-02",
        "Medication": "Paracetamol",
        "Test Results": "Normal"
    }

patients2_3 = [
    {
        "Name": "LesLie TErRy",
        "Age": 62,
        "Gender": "Male",
        "Blood Type": "A+",
        "Medical Condition": "Obesity",
        "Date of Admission": "2019-08-20",
        "Doctor": "Samantha Davies",
        "Hospital": "Kim Inc",
        "Insurance Provider": "Medicare",
        "Billing Amount": 33643.327286577885,
        "Room Number": 265,
        "Admission Type": "Emergency",
        "Discharge Date": "2019-08-26",
        "Medication": "Ibuprofen",
        "Test Results": "Inconclusive"
    },
    {
        "Name": "DaNnY sMitH",
        "Age": 76,
        "Gender": "Female",
        "Blood Type": "A-",
        "Medical Condition": "Obesity",
        "Date of Admission": "2022-09-22",
        "Doctor": "Tiffany Mitchell",
        "Hospital": "Cook PLC",
        "Insurance Provider": "Aetna",
        "Billing Amount": 27955.096078842456,
        "Room Number": 205,
        "Admission Type": "Emergency",
        "Discharge Date": "2022-10-07",
        "Medication": "Aspirin",
        "Test Results": "Normal"
    }
]

collection.insert_one(patient1)
collection.insert_many(patients2_3)
client.close()
