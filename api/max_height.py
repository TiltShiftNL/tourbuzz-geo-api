import json
from .database import SessionLocal
from .models import DbPoint, DbLine
from geoalchemy2 import func

def get_base_point_query():
    db = SessionLocal()
    return db.query(
        DbPoint.name,
        DbPoint.maxheight,
        DbPoint.way.ST_Transform(4326).ST_AsGeoJson())


def get_base_line_query():
    db = SessionLocal()
    return db.query(
        DbLine.name,
        DbLine.maxheight,
        DbLine.way.ST_Centroid().ST_Transform(4326).ST_AsGeoJson())


def construct_geojson(result):
    feature_collection = {
        "type": "FeatureCollection",
        "name": "max_height",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": []
    }
    for entry in result:
        if(entry[1] not in ['default', 'none', 'below_default']):
            # if entry[1] ends with m, remove spaces, else add m
            if(entry[1].endswith("m")):
                dh = entry[1].replace(" ", "").strip("m")
            else:
                dh = entry[1]
            out = {
                "type": "Feature",
                "properties": {
                    "title": entry[0] or "",
                    "maxheight_text": dh.strip("0").strip(".") + "m",
                    "maxheight": float(dh.strip("0").strip("."))
                },
                "geometry": json.loads(entry[2]),
            }
            feature_collection["features"].append(out)
    return feature_collection


def legacy():
    result_set = {
        "max_doorrijhoogtes": []
    }
    result = get_base_point_query().filter(DbPoint.maxheight.isnot(None)).all()
    for entry in result:
        # if entry[1] ends with m, remove spaces, else add m
        if(entry[1].endswith("m")):
            dh = entry[1].replace(" ", "").strip("m")
        else:
            dh = entry[1]
        out = {
            "max_doorrijhoogte": {
                "title": entry[0] or "",
                "Lokatie": entry[2],
                "Maximale_doorrijhoogte": dh.strip("0").strip(".") + "m"
            }
        }
        result_set["max_doorrijhoogtes"].append(out)
    return result_set


def geojson_bbox(bounds):
    bounds_parts = bounds.split(',')
    line_result = get_base_line_query().filter(DbLine.maxheight.isnot(None)).filter(
            func.ST_Intersects(
                func.ST_MakeEnvelope(
                    bounds_parts[0],
                    bounds_parts[1],
                    bounds_parts[2],
                    bounds_parts[3],
                    4326
                ),
                func.ST_Transform(func.ST_Centroid(DbLine.way),4326),
            )
        ).all()
    point_result = get_base_point_query().filter(DbPoint.maxheight.isnot(None)).filter(
            func.ST_Intersects(
                func.ST_MakeEnvelope(
                    float(bounds_parts[0]),
                    float(bounds_parts[1]),
                    float(bounds_parts[2]),
                    float(bounds_parts[3]),
                    4326
                ),
                func.ST_Transform(DbPoint.way,4326),
            )
        ).all()
    return construct_geojson(line_result + point_result)


def geojson_all():
    line_results = get_base_line_query().filter(DbLine.maxheight.isnot(None)).all()
    point_results = get_base_point_query().filter(DbPoint.maxheight.isnot(None)).all()
    return construct_geojson(line_results + point_results)
