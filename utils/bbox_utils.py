import pandas as pd


def get_center_of_bbox(bbox):
    if not bbox or len(bbox) != 4 or any(pd.isna(bbox)):
        return None  # Ball position unknown

    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return (cx, cy)

def get_bbox_width(bbox):

    x1, _, x2, _ = bbox
    return int(x2 - x1)


def measure_distance(p1, p2):
    

    if p1 is None or p2 is None:
        return float('inf')  # Impossible distance if missing
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
