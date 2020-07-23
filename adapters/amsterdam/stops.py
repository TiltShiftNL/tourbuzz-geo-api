from .settings import settings
import json
import urllib.request
from api.database import SessionLocal, engine
from api.models import DbStop
from geoalchemy2 import functions


def run():
    """
    Adapter to grab stops from the API of the City of Amsterdam
    via https://api.data.amsterdam.nl/dcatd/datasets/IuAYhr-__qZj9Q/purls/uEOyRO9EKBNIeA
    """
    connect_string = settings.AMSTERDAM_STOPS
    url = urllib.request.urlopen(connect_string)
    if url.getcode() == 200:
        data = url.read()
        # Start inserting
        result = json.loads(data)
        db = SessionLocal()

        try:
            DbStop.__table__.create(engine)
        except:
            pass

        for entry in result["in_uitstaphaltes"]:
            row = DbStop(
                source_url=settings.AMSTERDAM_STOPS,
                source_name="Amsterdam",
                source_id=entry["in_uitstaphalte"]["title"].split(":")[0],
                title=entry["in_uitstaphalte"]["title"],
                name=entry["in_uitstaphalte"]["title"].split(":")[1].strip(),
                description=entry["in_uitstaphalte"]["Bijzonderheden"],
                spots_text=entry["in_uitstaphalte"]["Busplaatsen"],
                spots=int(entry["in_uitstaphalte"]["Busplaatsen"].split(" ")[0]),
                point=functions.ST_GeomFromGeoJSON(entry["in_uitstaphalte"]["Lokatie"])

            )
            db.merge(row)
        db.commit()
