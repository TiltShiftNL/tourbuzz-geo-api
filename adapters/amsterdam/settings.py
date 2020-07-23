import os
from pydantic import HttpUrl, BaseSettings


class Settings(BaseSettings):
    AMSTERDAM_STOPS = os.environ.get('AMSTERDAM_STOPS', "https://api.data.amsterdam.nl/dcatd/datasets/IuAYhr-__qZj9Q/purls/uEOyRO9EKBNIeA")
    AMSTERDAM_PARKING = os.environ.get('AMSTERDAM_PARKING', "https://api.data.amsterdam.nl/dcatd/datasets/IuAYhr-__qZj9Q/purls/uB95bElRaUcD0A")


settings = Settings()
