def get_center_of_bbox(bbox):
    """
    Calculate the center of a bounding box.
    
    Args:
        bbox (list or tuple): Bounding box in the format [x1, y1, x2, y2].
        
    Returns:
        tuple: Center coordinates (cx, cy).
    """
    x1, y1, x2, y2 = bbox
    cx = int(x1 + x2) / 2
    cy = int(y1 + y2) / 2
    return cx, cy

def get_bbox_width(bbox):
    """
    Calculate the width of a bounding box.
    
    Args:
        bbox (list or tuple): Bounding box in the format [x1, y1, x2, y2].
        
    Returns:
        int: Width of the bounding box.
    """
    x1, _, x2, _ = bbox
    return int(x2 - x1)