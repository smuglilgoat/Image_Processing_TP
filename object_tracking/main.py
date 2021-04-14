import cv2
from tracker import *
import json

tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("pedestrians.avi")

objectDetector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=False)
results = {}

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    roi = frame[0:160, :]

    mask = objectDetector.apply(roi)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 500:
            x, y, w, h = cv2.boundingRect(c)
            detections.append([x, y, w, h])

    objects = tracker.update(detections, 85)
    for o in objects:
        x, y, w, h, id = o
        results[id] = {'x': x, 'y': y, 'w':w, 'h':h}
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.circle(roi, (x + w//2, y + h//2), 5, (0, 255, 0), -1)

    cv2.imshow("ROI", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        break

with open('result.json', 'w') as fp:
    json.dump(results, fp)
cap.release()
cv2.destroyAllWindows()