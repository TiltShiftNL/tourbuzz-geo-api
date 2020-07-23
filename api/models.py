from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Sequence
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from .database import Base

class DbParking(Base):
    __tablename__ = "parking"
    id = Column(Integer, Sequence('parking_id_seq'))
    source_url = Column(String)
    source_name = Column(String, primary_key=True, index=True)
    source_id = Column(String, primary_key=True, index=True)
    link_url = Column(String)
    link_title = Column(String)
    title = Column(String)
    name = Column(String)
    description = Column(String)
    spots_text = Column(String)
    spots = Column(Integer)
    point = Column(Geometry('POINT'))

class DbStop(Base):
    __tablename__ = "stops"
    id = Column(Integer, Sequence('stops_id_seq'))
    source_url = Column(String)
    source_name = Column(String, primary_key=True, index=True)
    source_id = Column(String, primary_key=True, index=True)
    link_url = Column(String)
    link_title = Column(String)
    title = Column(String)
    name = Column(String)
    description = Column(String)
    spots_text = Column(String)
    spots = Column(Integer)
    point = Column(Geometry('POINT'))


class DbPoint(Base):
    __tablename__ = "planet_osm_point"

    osm_id = Column(Integer, primary_key=True, index=True)
    access = Column(String)
    name = Column(String)
    maxheight = Column(String)
    way = Column(Geometry('POINT'))

class DbRoad(Base):
    __tablename__ = "planet_osm_roads"

    osm_id = Column(Integer, primary_key=True, index=True)
    access = Column(String)
    name = Column(String)
    maxheight = Column(String)
    way = Column(Geometry('LINESTRING'))


class DbLine(Base):
    __tablename__ = "planet_osm_line"

    osm_id = Column(Integer, primary_key=True, index=True)
    access = Column(String)
    name = Column(String)
    maxheight = Column(String)
    way = Column(Geometry('LINESTRING'))


class DbEnvironmentalZone(Base):
    __tablename__ = "environmental_zones"
    id = Column(Integer, Sequence('environmental_zones_id_seq'))
    source_url = Column(String)
    source_name = Column(String, primary_key=True, index=True)
    source_id = Column(String, primary_key=True, index=True)
    objectid = Column(Integer)
    gemeente = Column(String)
    website = Column(String)
    vrachtauto = Column(Integer)
    bestelauto = Column(Integer)
    personenauto = Column(Integer)
    taxi = Column(Integer)
    bromfiets = Column(Integer)
    autobus = Column(Integer)
    bron = Column(String)
    versie = Column(String)
    vrachtjaar = Column(String)
    besteljaar = Column(Integer)
    personenjaar = Column(Integer)
    taxijaar = Column(Integer)
    bromjaar = Column(Integer)
    autobusjaar = Column(Integer)

    wkb_geometry = Column(Geometry(srid=4326))