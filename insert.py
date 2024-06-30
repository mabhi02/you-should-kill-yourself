from pymongo import MongoClient
from bson import ObjectId
import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['EP']
log_collection = db['log']

# Updated JSON data
data = [
  {
    "_id": ObjectId("6680ff00f123456789abcdef"),
    "name": "Alice",
    "email": "alice@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJGxJN09NbzRBb1VQTEFiTVR2elQ4U21sbE9UQlFpM2h2UVhlN09ZdExEU0Q4cVdxdFRyNzhu", "subType": "00"}},
    "points": 10,
    "created_at": datetime.datetime.strptime("2024-06-29T23:40:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff01f123456789abcdef"),
    "name": "Bob",
    "email": "bob@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJEdGU2d2bm9WWnpLM0N5Z2x1UThHRWhQeHdESnU4Zmh0MXZFVVR2RHZ1c1hrVkF5RmFoM2V1", "subType": "00"}},
    "points": 20,
    "created_at": datetime.datetime.strptime("2024-06-29T23:41:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff02f123456789abcdef"),
    "name": "Charlie",
    "email": "charlie@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJGVXbW1EUVBKM1l1aE1QeFhRZTJHQlU5RGpOZ2lVc3Z2VzJtT3dMQXJ2L1JUbmxsWE9POTc2", "subType": "00"}},
    "points": 0,
    "created_at": datetime.datetime.strptime("2024-06-29T23:42:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff03f123456789abcdef"),
    "name": "David",
    "email": "david@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJG5IU3ZjRFh0ekI4Q1lObXkyT1J1ZGJpRVhRbHhFb3hNUjRFZm9sa2t4U1dGcmQzRGlFY0dF", "subType": "00"}},
    "points": 15,
    "created_at": datetime.datetime.strptime("2024-06-29T23:43:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff04f123456789abcdef"),
    "name": "Eve",
    "email": "eve@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJDJNS3RhMktVQnhiYm5DNGdBbUNncnZsVnI5Yk9IbmZ1cHZodW5qL29hRWliVVFsN3lyZXZr", "subType": "00"}},
    "points": 25,
    "created_at": datetime.datetime.strptime("2024-06-29T23:44:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff05f123456789abcdef"),
    "name": "Frank",
    "email": "frank@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJHJKc2hKZ1JIVDlEUTd0bFlUOE5CcXhUVGZBckV2UlhvNFFkQ1VGRHpaNGRFVmJUbWg3WjBB", "subType": "00"}},
    "points": 0,
    "created_at": datetime.datetime.strptime("2024-06-29T23:45:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff06f123456789abcdef"),
    "name": "Grace",
    "email": "grace@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJHR5VnVzdHh1TktMeHk4OGJaQ1ZvYkZXV1h4TFdoM2FpY2JLUjY5TFVQVE15T2M1RGpLRkpB", "subType": "00"}},
    "points": 5,
    "created_at": datetime.datetime.strptime("2024-06-29T23:46:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff07f123456789abcdef"),
    "name": "Hank",
    "email": "hank@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJHRubHVSbmhVM2swOGQ2VUtjV2VwM0FOMVlvUzNabkhMOGhObEFSdHFlcHJ3RlpueTBHd1Zk", "subType": "00"}},
    "points": 35,
    "created_at": datetime.datetime.strptime("2024-06-29T23:47:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff08f123456789abcdef"),
    "name": "Ivy",
    "email": "ivy@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJE5qSGhNeVp6NVoyTXM2VGJLa1FDaThwMnRQTnN2c2t5cW5DbzhndXBRT29EOTBsMFJvTG5a", "subType": "00"}},
    "points": 45,
    "created_at": datetime.datetime.strptime("2024-06-29T23:48:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff09f123456789abcdef"),
    "name": "Jack",
    "email": "jack@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJHNjcUxzcFdhbnNTeW5KQ3dETVdCS1BNM2dwV05kMFBNR1B6SVJSMkU4Tk5pWTRnTmdyRkU2", "subType": "00"}},
    "points": 55,
    "created_at": datetime.datetime.strptime("2024-06-29T23:49:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff0af123456789abcdef"),
    "name": "Kate",
    "email": "kate@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJEZJZ3RlNXBFZ1Bvc1NFV0VsSW9HbFp3cnNQTXd4SHQ0eVNCQ3NnQnRpSk9EMmdQRkREdVRO", "subType": "00"}},
    "points": 60,
    "created_at": datetime.datetime.strptime("2024-06-29T23:50:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff0bf123456789abcdef"),
    "name": "Leo",
    "email": "leo@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJEFSbk5sMmpVcUVmVkdUQVRHRHpka0VnM0pqeGVSMWlYN2xvZWFDL0lwblFzL05nMFlCS2sw", "subType": "00"}},
    "points": 50,
    "created_at": datetime.datetime.strptime("2024-06-29T23:51:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff0cf123456789abcdef"),
    "name": "Mia",
    "email": "mia@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJFN5TjB1dUV2U3pWblRqa1MxR2tUbzFFVGpKOHFjcGFuR0t1MUFaWUpmVWRoN0o4T0VVRExU", "subType": "00"}},
    "points": 30,
    "created_at": datetime.datetime.strptime("2024-06-29T23:52:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff0df123456789abcdef"),
    "name": "Nina",
    "email": "nina@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJHhrU2FuM1Q3MXBlVkhDU29NOG1uWkJLT3lhQ05SSGVpTWVhV0x2OHNoWmF5d1hhd1g1bGhG", "subType": "00"}},
    "points": 40,
    "created_at": datetime.datetime.strptime("2024-06-29T23:53:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff0ef123456789abcdef"),
    "name": "Oscar",
    "email": "oscar@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJHZhV29yS2Z3M0t6ZnVPaTlOT2tOVk96Z1Y1eVZpRFV1V09LRGJqRmdmMFUwWkZJNzFPNDlw", "subType": "00"}},
    "points": 20,
    "created_at": datetime.datetime.strptime("2024-06-29T23:54:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff0ff123456789abcdef"),
    "name": "Paul",
    "email": "paul@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJHpOc1JSVmZ3NVpUbFJncUxqT0tHRU9XT2FWR1BtUzdqRUZpMm5kNVUzMHRuN2NHVmJjNEJ1", "subType": "00"}},
    "points": 10,
    "created_at": datetime.datetime.strptime("2024-06-29T23:55:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff10f123456789abcdef"),
    "name": "Quincy",
    "email": "quincy@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJE5vTTFYN2J1L0V3U2J1VFpGS1R0MkU1NUNpdkdMTm5wNlNqczJNd05aTFJhZWhIZkUwbkE5", "subType": "00"}},
    "points": 0,
    "created_at": datetime.datetime.strptime("2024-06-29T23:56:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff11f123456789abcdef"),
    "name": "Rose",
    "email": "rose@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJG1ac0xIQ3RIT3d4N1Z1L3Q1aTFUVnhFQ1dBcFdVZktlTnQ2ZnBxalAxVUtubEdwbUhuSGtO", "subType": "00"}},
    "points": 10,
    "created_at": datetime.datetime.strptime("2024-06-29T23:57:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff12f123456789abcdef"),
    "name": "Steve",
    "email": "steve@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJHV4eXdLTFFQSzREa3Y0cVp3ZGhPQTFLWlFkUG44eGpDOVUyZ1V2b0hHR2gybm1GdTRTRHlY", "subType": "00"}},
    "points": 5,
    "created_at": datetime.datetime.strptime("2024-06-29T23:58:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  },
  {
    "_id": ObjectId("6680ff13f123456789abcdef"),
    "name": "Tina",
    "email": "tina@example.com",
    "password": {"$binary": {"base64": "JDJiJDEyJGxMYzFPYXdTZ2lTa0EyNlRkTmtIVmMyY2ZBZmd0RG9GRjM4NVB6bEV0dlBpWFltQUZ4dTVv", "subType": "00"}},
    "points": 15,
    "created_at": datetime.datetime.strptime("2024-06-29T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
  }
]

# Insert the data into the MongoDB collection
log_collection.insert_many(data)

print("Dummy users added successfully.")
