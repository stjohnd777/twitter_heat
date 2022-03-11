import json, logging


def get_centroid_from_bbox(bbox):
    """"
    Get centroid bbox
    """
    bbox = bbox.decode("utf-8")
    bbox = json.loads(bbox)
    bbox = bbox.decode("utf-8")
    bbox = json.loads(bbox)
    lat = (bbox[0] + bbox[2]) / 2
    lon = (bbox[1] + bbox[3]) / 2
    logging.info(f"geo centroid ({lat},{lon})")
    return (lat, lon)
