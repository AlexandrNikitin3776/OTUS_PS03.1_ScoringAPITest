#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import tarantool

# from scoringapi import api, scoring

SERVER_HOST = 'localhost'
SERVER_PORT = 3301
RECONNECT_MAX_ATTEMPTS = 5
RECONNECT_DELAY = 20
CONNECTION_TIMEOUT = 200


class Store:
    cache = {}

    def __init__(
        self,
        space,
        host=SERVER_HOST,
        port=SERVER_PORT,
        user=None,
        password=None,
        reconnect_max_attempts=RECONNECT_MAX_ATTEMPTS,
        reconnect_delay=RECONNECT_DELAY,
        connect_now=False,
        connection_timeout=CONNECTION_TIMEOUT,
    ):
        self.connection = tarantool.Connection(
            host=host,
            port=port,
            user=user,
            password=password,
            reconnect_max_attempts=reconnect_max_attempts,
            reconnect_delay=reconnect_delay,
            connect_now=False,
            connection_timeout=connection_timeout,
        )
        self.space = space

    def cache_get(self, key):
        cache = self.cache.get(key)
        if cache:
            value, storetime = cache
            if time.time() >= storetime:
                return value

    def cache_set(self, key, value, storetime):
        self.cache[key] = (value, time.time() + storetime)

    def get(self, key):
        response = self.connection.select(self.space, key)
        return response.data[0][1]

    def set(self, key, value):
        self.connection.replace(self.space, (key, value))


'''


4. Естественно нужно протестировать этот новый фунĸционал.
    Обратите внимание, фунĸции get_score не важна доступность store'а,
    она использует его ĸаĸ ĸэш и, следовательно, должна работать
    даже если store сгорел в верхних слоях атмосферы.
    get_interests использует store ĸаĸ персистентное хранилище
    и если со store'ом что-то случилось может отдавать тольĸо ошибĸи.
'''
