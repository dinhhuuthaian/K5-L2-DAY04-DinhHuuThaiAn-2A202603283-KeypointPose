import json, glob, os
from ultralytics import YOLO

NAMES = ["nose","left_eye","right_eye","left_ear","right_ear","left_shoulder",
 "right_shoulder","left_elbow","right_elbow","left_wrist","right_wrist","left_hip",
 "right_hip","left_knee","right_knee","left_ankle","right_ankle"]
SKEL = [[16,14],[14,12],[17,15],[15,13],[12,13],[6,12],[7,13],[6,7],[6,8],[7,9],
 [8,10],[9,11],[2,3],[1,2],[1,3],[2,4],[3,5],[4,6],[5,7]]

model = YOLO("yolo26n-pose.pt")
images, anns = [], []
for i, f in enumerate(sorted(glob.glob("data/persons/*.jpg")), 1):
    r = model(f, verbose=False)[0]
    h, w = r.orig_shape
    images.append({"id": i, "file_name": os.path.basename(f), "width": w, "height": h})
    if r.keypoints is None:
        continue
    xy = r.keypoints.xy.cpu().numpy()
    cf = r.keypoints.conf.cpu().numpy()
    bx = r.boxes.xyxy.cpu().numpy()
    for p in range(len(xy)):
        x1, y1, x2, y2 = [float(v) for v in bx[p]]
        if (y2 - y1) < 60:          # luật 60 px của lab
            continue
        kps, n = [], 0
        for k in range(17):
            x, y = float(xy[p][k][0]), float(xy[p][k][1])
            if cf[p][k] > 0.5 and 0 <= x < w and 0 <= y < h:
                kps += [round(x, 1), round(y, 1), 2]; n += 1
            else:
                kps += [0, 0, 0]
        anns.append({"id": len(anns) + 1, "image_id": i, "category_id": 1,
                     "keypoints": kps, "num_keypoints": n, "iscrowd": 0,
                     "bbox": [x1, y1, x2 - x1, y2 - y1],
                     "area": (x2 - x1) * (y2 - y1)})

coco = {"images": images, "annotations": anns,
        "categories": [{"id": 1, "name": "person", "keypoints": NAMES, "skeleton": SKEL}]}
json.dump(coco, open("model_persons.json", "w"))
print(len(images), "ảnh,", len(anns), "người")