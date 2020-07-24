FROM python:3.8.3-slim

WORKDIR /usr/src/app

LABEL maintainer="Milo van der Linden - https://www.tiltshiftapps.nl"

ENV SQL_ALCHEMY_DATABASE_URL "postgresql://postgres:mysecretpassword@localhost/gis"
ENV GOOGLE_MAPS_KEY yourgooglemapskeyhere
ENV BACKEND_CORS_ORIGINS "http://localhost,http://localhost:4200,http://localhost:3000"
ENV IPO_ENVIRONMENTAL_ZONES "https://services.arcgis.com/kE0BiyvJHb5SwQv7/ArcGIS/rest/services/Milieuzones_NL/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token="
ENV AMSTERDAM_STOPS "https://api.data.amsterdam.nl/dcatd/datasets/IuAYhr-__qZj9Q/purls/uEOyRO9EKBNIeA"
ENV AMSTERDAM_PARKING "https://api.data.amsterdam.nl/dcatd/datasets/IuAYhr-__qZj9Q/purls/uB95bElRaUcD0A"

RUN apt-get update && apt-get install -y \
    postgresql-client

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
VOLUME ["/usr/src/app/data"]
CMD [ "python", "./tourbuzz.py" ]