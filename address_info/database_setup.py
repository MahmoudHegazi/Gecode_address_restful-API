











#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), primary_key=True)


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    user_input = Column(String(255))
    request_status = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user_input': self.user_input,
            'user_id': self.user_id,
            'request_status': self.request_status,
        }


class Results(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    latitude  = Column(String(250), nullable=False)
    longitude = Column(String(250), nullable=False)
    formatted_address = Column(String(255), nullable=False)
    place_id = Column(String(255), nullable=False)
    long_name = Column(String(255), nullable=False)
    types = Column(String(255), nullable=False)
    request_id = Column(Integer, ForeignKey('request.id'))
    request = relationship(Request)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.menu_type,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'formatted_address': self.formatted_address,
            'place_id': self.place_id,
            'long_name': self.long_name,
            'request_id': self.request_id,
            'types': self.types
        }


class RequestError(Base):
    __tablename__ = 'request_error'

    id = Column(Integer, primary_key=True)
    user_input = Column(String(255))
    request_status = Column(String(255))
    error_message = Column(String(255))
    request_id = Column(Integer, ForeignKey('request.id'))
    request = relationship(Request)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.name,
            'user_input': self.user_input,
            'request_status': self.request_status,
            'error_message': self.error_message,
            'request_id': self.request_id
        }
engine = create_engine('sqlite:///address_info.db')
Base.metadata.create_all(engine)
