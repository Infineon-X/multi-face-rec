import face_recognition
import pickle
from pathlib import Path

def recognize_faces(image_path):
    """recognize faces in an image"""

    # load saved face encodings
    with open("encodings.pkl", "rb") as f:
        loaded_encodings = pickle.load(f)

    print(f"\nloaded {len(loaded_encodings['encodings'])} face codes")
    print(f"checking out this image: {image_path}\n")

    # load the image to check
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_face_locations = face_recognition.face_locations(unknown_image)
    unknown_encodings = face_recognition.face_encodings(unknown_image, unknown_face_locations)

    print(f"found {len(unknown_encodings)} face(s) in the image\n")

    # compare unknown faces to known faces
    for i, unknown_encoding in enumerate(unknown_encodings):
        results = face_recognition.compare_faces(
            loaded_encodings["encodings"],
            unknown_encoding,
            tolerance=0.6
        )

        # collect matching names
        matches = []
        for j, match in enumerate(results):
            if match:
                matches.append(loaded_encodings["names"][j])

        if matches:
            # find most common name in matches
            most_common = max(set(matches), key=matches.count)
            print(f"face {i+1}: looks like {most_common}")
        else:
            print(f"face {i+1}: don't know who this is")

if __name__ == "__main__":
    # test with one image

    test_image = "test_images/test2.jpg"
    recognize_faces(test_image)
