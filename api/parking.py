import json
from .models import DbParking
from .database import SessionLocal, engine
from .settings import settings
from geoalchemy2 import func


def get_base_query():
    db = SessionLocal()
    return db.query(
        DbParking.id,
        DbParking.source_url,
        DbParking.source_name,
        DbParking.source_id,
        DbParking.link_url,
        DbParking.link_title,
        DbParking.name,
        DbParking.title,
        DbParking.description,
        DbParking.spots_text,
        DbParking.spots,
        DbParking.point.ST_Transform(4326).ST_AsGeoJson())

def construct_geojson(result):
    feature_collection = {
        "type": "FeatureCollection",
        "name": "maxheight",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": []
    }
    for entry in result:
        out = {
               "type": "Feature",
               "id": entry[0],
               "properties": {
                   "title": entry[7],
                   "name": entry[6],
                   "description": entry[8],
                   "spots_text": entry[9],
                   "spots": entry[10],
                   "link": {
                        "url":  entry[4],
                        "title":  entry[5],
                    },
                    "source": {
                        "name": entry[2],
                        "url": entry[1],
                        "id": entry[3]
                    }
               },
               "geometry": json.loads(entry[11])
           }
        feature_collection["features"].append(out)
    return feature_collection


def legacy():
    result_set = {
        "parkeerplaatsen": {}
    }
    try:
        result = get_base_query().all()
    except:
        DbParking.__table__.create(engine)
        result = get_base_query().all()

    for entry in result:
        point = json.loads(entry[11])
        out = {
            "nummer": entry[3],
            "naam": entry[6],
            "capaciteit": entry[10],
            "location": {
                "lat": point["coordinates"][1],
                "lng": point["coordinates"][0]
            },
            "mapsImageUrl": "https://maps.googleapis.com/maps/api/staticmap?center=" + \
                str(point["coordinates"][1]) + "," + str(point["coordinates"][0]) + \
                "&zoom=16&size=600x300&maptype=roadmap&markers=" + \
                str(point["coordinates"][1]) + "," + str(point["coordinates"][0]) + \
                "&key=" + settings.GOOGLE_MAPS_KEY,
            "mapsUrl": "https://www.google.com/maps/?q=loc:" + \
                str(point["coordinates"][1]) + "," + str(point["coordinates"][0]),
            "beschikbaar": True,
            "vialis": None,
            "_origineel": {
                "title": entry[7],
                "Lokatie": entry[11],
                "Bijzonderheden": entry[8],
                "Busplaatsen": entry[9],
                "linkurl": entry[4],
                "linknaam": entry[5]
            }
        }
        result_set["parkeerplaatsen"][entry[3]] = out
    return result_set


def geojson_bbox(bounds):
    bounds_parts = bounds.split(',')
    result = get_base_query().filter(
            func.ST_Intersects(
                func.ST_MakeEnvelope(
                    bounds_parts[0],
                    bounds_parts[1],
                    bounds_parts[2],
                    bounds_parts[3],
                    4326
                ),
                DbParking.point.ST_Transform(4326),
            )
        ).all()
    return construct_geojson(result)


def geojson_all():
    
    try:
        result = get_base_query().all()
    except:
        DbParking.__table__.create(engine)
        result = get_base_query().all()
    return construct_geojson(result)
