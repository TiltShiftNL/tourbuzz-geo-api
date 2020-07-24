import os
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    SQL_ALCHEMY_DATABASE_URL = os.environ.get('SQL_ALCHEMY_DATABASE_URL', "postgresql://postgres:mysecretpassword@localhost/gis")
    GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY', "googlemapskeyhere)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [x.strip() for x in os.environ.get(
        'BACKEND_CORS_ORIGINS', "http://localhost,http://localhost:4200,http://localhost:3000").split(',')]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
