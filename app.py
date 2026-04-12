import face_recognition
import pickle
import cv2
import numpy as np
from pathlib import Path

ENCODINGS_PATH = "encodings/face_encodings.pkl"
DATASET_PATH   = "dataset"

# Model Training ........
def train_model():
    known_encodings, known_names = [], []
    dataset = Path(DATASET_PATH)

    for student_dir in dataset.iterdir():
        if not student_dir.is_dir():
            continue
        for img_path in student_dir.glob("*.jpg"):
            img = face_recognition.load_image_file(str(img_path))
            locs = face_recognition.face_locations(img, model="hog")
            encs = face_recognition.face_encodings(img, locs)
            for enc in encs:
                known_encodings.append(enc)
                known_names.append(student_dir.name)   # folder = roll_no

    Path("encodings").mkdir(exist_ok=True)
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)
    return len(known_names)

# Loading 
def load_encodings():
    if not Path(ENCODINGS_PATH).exists():
        return [], []
    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)
    return data["encodings"], data["names"]

# Recognition
def recognize_faces(frame, known_encodings, known_names, tolerance=0.50):
    rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small = cv2.resize(rgb, (0, 0), fx=0.5, fy=0.5)

    boxes = face_recognition.face_locations(small, model="hog")
    encs  = face_recognition.face_encodings(small, boxes)

    results = []
    for enc, box in zip(encs, boxes):
        name, confidence = "Unknown", 0.0
        distances = face_recognition.face_distance(known_encodings, enc)

        if len(distances):
            best = np.argmin(distances)
            if distances[best] <= tolerance:
                name       = known_names[best]
                confidence = round((1 - distances[best]) * 100, 1)

        top, right, bottom, left = [v * 2 for v in box]
        results.append({
            "name": name,
            "confidence": confidence,
            "box": (top, right, bottom, left)
        })
    return results

# Draw ...
def draw_results(frame, results):
    for r in results:
        t, ri, b, l = r["box"]
        color = (0, 200, 0) if r["name"] != "Unknown" else (0, 0, 220)
        cv2.rectangle(frame, (l, t), (ri, b), color, 2)
        label = f"{r['name']}  {r['confidence']}%"
        cv2.rectangle(frame, (l, b - 28), (ri, b), color, cv2.FILLED)
        cv2.putText(frame, label, (l + 4, b - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    return frame