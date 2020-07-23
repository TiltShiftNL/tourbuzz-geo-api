from .settings import settings
import json
import geojson
from shapely.geometry import shape
import urllib.request
from api.database import SessionLocal, engine
from api.models import DbEnvironmentalZone
from geoalchemy2 import functions


def run():
    """
    Adapter to grab environmental zones from some obscure esri server
    """
    connect_string = settings.IPO_ENVIRONMENTAL_ZONES
    url = urllib.request.urlopen(connect_string)
    if url.getcode() == 200:
        data = url.read()
        # Start inserting
        result = json.loads(data)
        db = SessionLocal()

        try:
            DbEnvironmentalZone.__table__.create(engine)
        except:
            pass

        for entry in result["features"]:
            entry["crs"] = "EPSG:4326"
            geom = json.dumps(entry["geometry"])
            g1 = geojson.loads(geom)
            g2 = shape(g1)
            geom_wkb = g2.wkb

            row = DbEnvironmentalZone(
                source_url=settings.IPO_ENVIRONMENTAL_ZONES,
                source_name="kE0BiyvJHb5SwQv7",
                source_id=str(entry["id"]),
                objectid = entry["properties"]["OBJECTID"],
                gemeente = entry["properties"]["Gemeente"],
                website = entry["properties"]["website"],
                vrachtauto = entry["properties"]["vrachtauto"],
                bestelauto = entry["properties"]["bestelauto"],
                personenauto = entry["properties"]["personenauto"],
                taxi = entry["properties"]["taxi"],
                bromfiets = entry["properties"]["bromfiets"],
                autobus = entry["properties"]["autobus"],
                bron = entry["properties"]["bron"],
                versie = entry["properties"]["versie"],
                vrachtjaar = entry["properties"]["vrachtjaar"],
                besteljaar = entry["properties"]["besteljaar"],
                personenjaar = entry["properties"]["personenjaar"],
                taxijaar = entry["properties"]["taxijaar"],
                bromjaar = entry["properties"]["bromjaar"],
                autobusjaar = entry["properties"]["autobusjaar"],
                wkb_geometry = functions.ST_GeomFromWKB(geom_wkb, 4326)
            )
            db.merge(row)
        db.commit()
