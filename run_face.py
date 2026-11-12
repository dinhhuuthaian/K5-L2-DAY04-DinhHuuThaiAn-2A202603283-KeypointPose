import json, glob, os, urllib.request
import cv2
import mediapipe as mp

MODEL = "face_landmarker.task"
URL = ("https://storage.googleapis.com/mediapipe-models/face_landmarker/"
       "face_landmarker/float16/1/face_landmarker.task")
if not os.path.exists(MODEL):
    print("Đang tải model...")
    urllib.request.urlretrieve(URL, MODEL)

NAMES = ["left_eye_outer","left_eye_inner","left_eye_upper","left_eye_lower",
 "right_eye_outer","right_eye_inner","right_eye_upper","right_eye_lower",
 "nose_tip","mouth_left","mouth_right","lip_upper","lip_lower"]
# chỉ số điểm trong Face Mesh, cùng thứ tự với NAMES
IDX = [263,362,386,374, 33,133,159,145, 1, 291,61, 0,17]
SKEL = [[1,3],[2,3],[1,4],[2,4],[5,7],[6,7],[5,8],[6,8],
        [10,12],[11,12],[10,13],[11,13],[9,12]]

options = mp.tasks.vision.FaceLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=MODEL),
    running_mode=mp.tasks.vision.RunningMode.IMAGE, num_faces=1)

files = []
for pat in ("*.jpg", "*.jpeg", "*.png"):
    files += glob.glob("data/faces/" + pat)

images, anns = [], []
with mp.tasks.vision.FaceLandmarker.create_from_options(options) as lmk:
    for i, f in enumerate(sorted(files), 1):
        img = cv2.imread(f)
        h, w = img.shape[:2]
        images.append({"id": i, "file_name": os.path.basename(f), "width": w, "height": h})
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = lmk.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
        if not res.face_landmarks:
            print("Không thấy mặt:", os.path.basename(f))
            continue
        lm = res.face_landmarks[0]
        kps, xs, ys = [], [], []
        for k in IDX:
            x, y = lm[k].x * w, lm[k].y * h
            if 0 <= x < w and 0 <= y < h:
                kps += [round(x, 1), round(y, 1), 2]
                xs.append(x); ys.append(y)
            else:
                kps += [0, 0, 0]
        bw, bh = max(xs) - min(xs), max(ys) - min(ys)
        anns.append({"id": len(anns) + 1, "image_id": i, "category_id": 1,
                     "keypoints": kps,
                     "num_keypoints": sum(1 for v in kps[2::3] if v > 0),
                     "iscrowd": 0, "bbox": [min(xs), min(ys), bw, bh],
                     "area": bw * bh})

coco = {"images": images, "annotations": anns,
        "categories": [{"id": 1, "name": "face", "keypoints": NAMES, "skeleton": SKEL}]}
json.dump(coco, open("model_faces.json", "w"))
print(len(images), "ảnh,", len(anns), "mặt")