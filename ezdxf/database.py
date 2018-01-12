# Purpose: database module
# Created: 11.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .tools.binarydata import compress_binary_data
from .tools.handle import HandleGenerator
from .lldxf.const import DXFValueError
from .lldxf.tags import DXFTag


def factory():
    return EntityDB()


class EntityDB(object):
    """ A simple key/value database a.k.a. dict(), but can be replaced by other
    classes that implements all of the methods of `EntityDB`. The entities
    have no order.

    The Data Model

    Every entity/object, except tables and sections, are represented as
    tag-list (see Tags Class), this lists are stored in the drawing-associated
    database, database-key is the 'handle' tag (code == 5 or 105).

    For the entity/object manipulation this tag-list will be wrapped into
    separated classes, which are generated by the dxffactory-object.
    The dxffactory-object generates DXF-Version specific wrapper classes.

    """
    def __init__(self):
        self._database = {}
        self.handles = HandleGenerator()

    def __delitem__(self, key):
        del self._database[key]

    def __getitem__(self, handle):
        return self._database[handle]

    def get(self, handle, default=None):
        try:
            return self.__getitem__(handle)
        except KeyError:  # internal exception
            return default

    def __setitem__(self, handle, entity):
        self._database[handle] = entity

    def __contains__(self, handle):
        """ Database contains handle? """
        return handle in self._database

    def __len__(self):
        """ Count of database items. """
        return len(self._database)

    def __iter__(self):
        """ Iterate over all handles. """
        return iter(self._database.keys())

    def keys(self):
        """ Iterate over all handles. """
        return self._database.keys()

    def values(self):
        """ Iterate over all entities. """
        return self._database.values()

    def items(self):
        """ Iterate over all (handle, entities) pairs. """
        return self._database.items()

    def add_tags(self, tags):
        try:
            handle = tags.get_handle()
        except DXFValueError:  # create new handle
            handle = self.get_unique_handle()
            handle_code = 105 if tags.dxftype() == 'DIMSTYLE' else 5  # legacy shit!!!
            tags.noclass.insert(1, DXFTag(handle_code, handle))  # handle should be the 2. tag

        self.__setitem__(handle, tags)
        return handle

    def delete_entity(self, entity):
        entity.destroy()
        self.delete_handle(entity.dxf.handle)

    def delete_handle(self, handle):
        del self._database[handle]

    def compress_binary_data(self):
        for tags in self.values():
            compress_binary_data(tags)

    def get_unique_handle(self):
        while True:
            handle = self.handles.next()
            if handle not in self._database:  # you can not trust $HANDSEED value
                return handle

