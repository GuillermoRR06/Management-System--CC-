import json

def SaveData(data):
    with open("Data\data.json", "w") as Data:
        json.dump(data, Data, indent=4, ensure_ascii=True)

def Update_Time() -> None:
    pass