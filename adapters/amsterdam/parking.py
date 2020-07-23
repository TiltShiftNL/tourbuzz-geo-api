from .settings import settings
import json
import urllib.request
from api.database import SessionLocal, engine
from api.models import DbParking
from geoalchemy2 import functions


def run():
    """
    Adapter to grab parking from the API of the City of Amsterdam
    via https://api.data.amsterdam.nl/dcatd/datasets/IuAYhr-__qZj9Q/purls/uB95bElRaUcD0A
    """
    connect_string = settings.AMSTERDAM_PARKING
    url = urllib.request.urlopen(connect_string)
    if url.getcode() == 200:
        data = url.read()
        # Start inserting
        result = json.loads(data)
        db = SessionLocal()

        try:
            DbParking.__table__.create(engine)
        except:
            pass

        for entry in result["parkeerplaatsen"]:
            row = DbParking(
                source_name="Amsterdam",
                source_url=settings.AMSTERDAM_PARKING,
                source_id=entry["parkeerplaats"]["title"].split(":")[0],
                link_url=entry["parkeerplaats"]["linkurl"],
                link_title=entry["parkeerplaats"]["linknaam"],
                title=entry["parkeerplaats"]["title"],
                name=entry["parkeerplaats"]["title"].split(":")[1].strip(),
                description=entry["parkeerplaats"]["Bijzonderheden"],
                spots_text=entry["parkeerplaats"]["Busplaatsen"],
                spots=int(entry["parkeerplaats"]["Busplaatsen"].split(" ")[0]),
                point=functions.ST_GeomFromGeoJSON(entry["parkeerplaats"]["Lokatie"])

            )
            db.merge(row)
        db.commit()
