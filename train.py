import face_recognition
from pathlib import Path
import pickle

def train_faces():
    """make face codes from pics"""
    names = []
    encodings = []

    print("loading imgs...")

    for fp in Path("training").glob("*/*"):
        name = fp.parent.name
        print(f"- {name}: {fp.name}")

        img = face_recognition.load_image_file(fp)
        locs = face_recognition.face_locations(img, model="hog")
        codes = face_recognition.face_encodings(img, locs)

        for code in codes:
            names.append(name)
            encodings.append(code)

    print(f"\ngot {len(encodings)} faces")
    out = {"names": names, "encodings": encodings}

    with open("encodings.pkl", "wb") as f:
        pickle.dump(out, f)
    print("done. saved as encodings.pkl")

if __name__ == "__main__":
    train_faces()
