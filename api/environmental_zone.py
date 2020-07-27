import json
from .database import SessionLocal, engine
from .models import DbEnvironmentalZone
from geoalchemy2 import func


def get_base_query():
    db = SessionLocal()
    return db.query(
        DbEnvironmentalZone.id,
        DbEnvironmentalZone.objectid,
        DbEnvironmentalZone.wkb_geometry.ST_Transform(4326).ST_AsGeoJson(),
        DbEnvironmentalZone.gemeente,
        DbEnvironmentalZone.website,
        DbEnvironmentalZone.vrachtauto,
        DbEnvironmentalZone.bestelauto,
        DbEnvironmentalZone.personenauto,
        DbEnvironmentalZone.taxi,
        DbEnvironmentalZone.bromfiets,
        DbEnvironmentalZone.autobus,
        DbEnvironmentalZone.bron,
        DbEnvironmentalZone.versie,
        DbEnvironmentalZone.vrachtjaar,
        DbEnvironmentalZone.besteljaar,
        DbEnvironmentalZone.personenjaar,
        DbEnvironmentalZone.taxijaar,
        DbEnvironmentalZone.bromjaar,
        DbEnvironmentalZone.autobusjaar)


def construct_geojson(result):
    feature_collection = {
        "type": "FeatureCollection",
        "name": "environmental_zones",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": []
    }

    for entry in result:
        feature = {"type": "Feature", "properties": {
            "ogc_fid": str(entry[0]),
            "id": str(entry[1]),
            "municipality": entry[3],
            "url": entry[4],
            "truck": {
                "value": entry[5],
                "year": entry[12]
            },
            "delivery": {
                "value": entry[6],
                "year": entry[13]
            },
            "car": {
                "value": entry[7],
                "year": entry[14]
            },
            "taxi": {
                "value": entry[8],
                "year": entry[15]
            },
            "moped": {
                "value": entry[9],
                "year": entry[16]
            },
            "autobus": {
                "value": entry[10],
                "year": entry[17]
            },
            "source": entry[11],
            "version": entry[12]
        }, "geometry": json.loads(entry[2])}
        feature_collection["features"].append(feature)

    return feature_collection

def legacy():
    try:
        result = get_base_query().filter(DbEnvironmentalZone.gemeente == "Amsterdam").all()
    except:
        DbEnvironmentalZone.__table__.create(engine)
        result = get_base_query().filter(DbEnvironmentalZone.gemeente == "Amsterdam").all()

    feature_collection = {
        "type": "FeatureCollection",
        "name": "milieuzones",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": []
    }
    for entry in result:
        feature = {"type": "Feature", "properties": {
            "ogc_fid": str(entry[0]),
            "id": str(entry[1]),
            "verkeerstype": "vracht",
            "vanafdatum": "2008-01-01",
            "color": "#772b90"
        }, "geometry": json.loads(entry[2])}
        feature_collection["features"].append(feature)

    return feature_collection


def geojson_bbox(bounds):
    bounds_parts = bounds.split(',')
    result = get_base_query().filter(
            func.ST_Crosses(
                func.ST_MakeEnvelope(
                    bounds_parts[0],
                    bounds_parts[1],
                    bounds_parts[2],
                    bounds_parts[3],
                    4326
                ),
                DbEnvironmentalZone.wkb_geometry.ST_Transform(4326),
            )
        ).all()
    return construct_geojson(result)


def geojson_all():
    try:
        result = get_base_query().all()
    except:
        DbEnvironmentalZone.__table__.create(engine)
        result = get_base_query().all()
    return construct_geojson(result)

    
