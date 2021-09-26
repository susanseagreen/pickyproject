from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from django.core.files.storage import FileSystemStorage
import csv
import json
import os
import datetime


path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get("file_uploaded")
        fs = FileSystemStorage()
        filename = fs.save(f"src/uploads/{file_uploaded.name}", file_uploaded)
        with fs.open(filename, "rt") as txt_file:
            read_txt = csv.reader(txt_file, delimiter=",")
            time_list = build_csv(read_txt)

        if time_list:
            get_stats(time_list)
            ordered_time_list = order_data(time_list)
            unique_value = datetime.datetime.now().microsecond

            if self.basename == "download_csv":
                download_csv(self, unique_value, ordered_time_list)
            else:
                download_json(self, unique_value, ordered_time_list)
            return Response(ordered_time_list)

        return Response("GET API")


def build_csv(read_txt):
    time_list = {}

    for row in read_txt:
        for person in row:
            if ":" in person:
                name, time = person.split(":")
                name = clean_data(name)
                time = int(clean_data(time))
                if time < 0:
                    time = time * -1
                if name not in time_list:
                    time_list[name] = {}
                    time_list[name]["times"] = []
                    time_list[name]["total"] = 0
                time_list[name]["times"].append(time)
                time_list[name]["total"] += time

    return time_list


def clean_data(data):
    return data.replace(" ", "").lower()


def get_stats(time_list):
    for name in time_list:
        time_list[name]["avg"] = average(time_list[name]["times"])
        time_list[name]["high"] = max(time_list[name]["times"])
        time_list[name]["low"] = min(time_list[name]["times"])
        time_list[name]["count"] = len(time_list[name]["times"])


def average(num):
    return sum(num) / len(num)


def order_data(time_list):
    new_time_list = {}
    for num in range(len(time_list)):
        new_time_list[num] = {}

    x = 0
    for name in time_list:
        new_time_list[x]["name"] = name
        new_time_list[x]["total"] = str(datetime.timedelta(minutes=time_list[name]["total"]))
        new_time_list[x]["avg"] = str(datetime.timedelta(minutes=time_list[name]["avg"]))
        new_time_list[x]["high"] = str(datetime.timedelta(minutes=time_list[name]["high"]))
        new_time_list[x]["low"] = str(datetime.timedelta(minutes=time_list[name]["low"]))
        new_time_list[x]["count"] = time_list[name]["count"]
        x = x + 1

    return sorted(new_time_list.values(), key=lambda item: item["total"], reverse=True)


def download_csv(self, unique_value, time_list):

    directory = f"src/downloads/csv/picky_list_{unique_value}.csv"

    with open(directory, "w") as csvFile:
        writer = csv.writer(csvFile, delimiter=",")
        writer.writerow([
            "Name", "Total", "Average", "Highest", "Lowest", "Count"
        ])
        for time in time_list:
            writer.writerow([
                time["name"],
                time["total"],
                time["avg"],
                time["high"],
                time["low"],
                time["count"]
            ])
    os.startfile(os.path.join(path, directory))

    return


def download_json(self, unique_value, time_list):
    directory = f"src/downloads/json/picky_list_{unique_value}.json"
    with open(directory, "w") as outfile:
        json.dump(time_list, outfile, indent=4)

    if self.basename == "download_json":
        os.startfile(os.path.join(path, directory))

    return
