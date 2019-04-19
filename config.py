#!/usr/bin/env python3
import json
import os

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class Config(metaclass=Singleton):
    def __init__(self):
        try:
            with open('rain_check.json') as data_file:
                self.config = json.load(data_file)
        except FileNotFoundError:
            print("Failed to open configuration, create the configuration file: rain_check.json")
            sys.exit()
        except ValueError:
            print("Failed to parse configuration")
            sys.exit()