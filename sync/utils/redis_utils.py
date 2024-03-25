#!/usr/bin/env python3

"""Contains RedisHandler class"""

import redis
from datetime import timedelta
import json
from os import getenv
from dotenv import load_dotenv
load_dotenv()

HOST = getenv('REDIS_HOST')
PORT = getenv('REDIS_PORT')
PASSWORD = getenv('REDIS_PASSWORD')
MODE = getenv('MODE')


class RedisClient:
    """
    Redis Client class
    """

    def __init__(self, db=0):
        if MODE == 'production':
            self.redis_client = redis.StrictRedis(host=HOST, port=PORT, db=db, password=PASSWORD)
        else:
            self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=db)

    def status(self):
        """
        Returns the status of the redis server
        """
        return self.redis_client.ping()

    def set_key(self, key, value, expiry=None):
        """
        Sets a key in redis
        @param key: The key to set
        @param value: The value to set
        @param expiry: The expiry time in seconds
        """
        try:
            if expiry:
                serialized_value = json.dumps(value)
                self.redis_client.setex(key, timedelta(minutes=expiry), serialized_value)
            else:
                serialized_value = json.dumps(value)
                self.redis_client.set(key, serialized_value)
            return True
        except redis.RedisError as e:
            print(f"Error setting key '{key}' in Redis: {e}")

    def get_key(self, key):
        """
        Gets a key from redis
        @param key: The key to get
        """
        try:
            value_bytes = self.redis_client.get(key)
            if value_bytes:
                value_str = value_bytes.decode('utf-8')
                return json.loads(value_str)
            return None
        except redis.RedisError as e:
            print(f"Error getting key '{key}' from Redis: {e}")
            return None

    def delete_key(self, key):
        """
        Deletes a key from redis
        @param key: The key to delete
        """
        try:
            self.redis_client.delete(key)
            return True
        except redis.RedisError as e:
            print(f"Error deleting key '{key}' from Redis: {e}")

    def filter_delete_keys(self, query):
        """
        Deletes keys from redis that match a filter
        @param query: The filter to match
        """
        try:
            keys = self.redis_client.scan_iter(match=query)
            for key in keys:
                self.redis_client.delete(key)
            return True
        except redis.RedisError as e:
            print(f"Error deleting keys from Redis: {e}")