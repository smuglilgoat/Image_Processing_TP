import math


class EuclideanDistTracker:
    def __init__(self):
        self.centers = {}
        self.ids = 0

    def update(self, region, distTreshold):
        objects = []

        for rect in region:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            newObject = False
            for id, pt in self.centers.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < distTreshold:
                    self.centers[id] = (cx, cy)
                    print(self.centers)
                    objects.append([x, y, w, h, id])
                    newObject = True
                    break

            if newObject is False:
                self.centers[self.ids] = (cx, cy)
                objects.append([x, y, w, h, self.ids])
                self.ids += 1

        newCenters = {}
        for o in objects:
            _, _, _, _, id = o
            center = self.centers[id]
            newCenters[id] = center

        self.centers = newCenters.copy()
        return objects
