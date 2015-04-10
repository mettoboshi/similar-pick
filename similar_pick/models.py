# -*- coding: utf-8 -*-

class Restaurant(object):

    def __init__(self, id, name, rank, address, url):
        self.id = id
        self.name = name
        self.rank = rank
        self.address = address
        self.url = url

    def __repr__(self):
        return "<Restaurant('%s', '%s', '%s', '%s')>" % (self.id, self.name, self.address, self.url)
