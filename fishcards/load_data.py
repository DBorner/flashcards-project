import json
import os
import django
import shutil

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishcards.settings")
django.setup()

from main.models import FishCardSet, FishCard


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def create_card_set(data):
    card_set = FishCardSet.objects.create(
        name=data["name"],
        description=data["description"],
        image=data["image"],
    )
    for card in data["cards"]:
        FishCard.objects.create(
            question=card["question"],
            answer=card["answer"],
            fishcardset=card_set,
        )


def scan_card_sets():
    dir = os.path.join(os.getcwd(), "card_sets")
    for file in os.listdir(dir):
        if file.endswith(".json"):
            create_card_set(load_data(os.path.join(dir, file)))


def load_media_files_from_zip():
    dir = os.path.join(os.getcwd(), "card_sets")
    server_dir = os.path.join(os.getcwd(), "fishcards", "media")
    if os.path.exists("card_sets/media.zip"):
        shutil.unpack_archive("card_sets/media.zip", server_dir)


if __name__ == "__main__":
    print("Loading media files...")
    scan_card_sets()
    choice = input("Do you want to load media files from zip? (y/n): ")
    if choice.lower() == "y":
        load_media_files_from_zip()
    print("Done!")
