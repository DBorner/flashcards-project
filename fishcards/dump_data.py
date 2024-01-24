import json
import os
import django
import shutil

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishcards.settings")
django.setup()

from main.models import FishCardSet, FishCard


def dump_fish_card_sets():
    data = []
    for card_set in FishCardSet.objects.all():
        if FishCard.objects.filter(fishcardset=card_set).count() == 0:
            continue
        cards = []
        for card in FishCard.objects.filter(fishcardset=card_set):
            cards.append(
                {
                    "question": card.question,
                    "answer": card.answer,
                }
            )
        data.append(
            {
                "name": card_set.name,
                "description": card_set.description,
                "image": card_set.image.url if card_set.image else None,
                "cards": cards,
            }
        )
    for index, card_set in enumerate(data):
        with open(f"card_sets/{index}.json", "w", encoding="utf-8") as f:
            json.dump(card_set, f, indent=4, ensure_ascii=False)


def save_all_media_files_to_zip():
    dir = os.path.join(os.getcwd(), "fishcards", "media")
    if os.path.exists("card_sets/media"):
        shutil.make_archive("card_sets/media", "zip", dir)


if __name__ == "__main__":
    print("Dumping media files...")
    dump_fish_card_sets()
    save_all_media_files_to_zip()
    print("Done!")
