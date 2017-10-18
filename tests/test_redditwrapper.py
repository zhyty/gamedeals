'''Test module for reddit wrapper functions.'''
import json

import pytest

from gamedeals import redditwrapper
from . import SAMPLE_NEW_JSON

def test_listing_filtering():
    '''Filtered keys should match exactly.'''
    with open(SAMPLE_NEW_JSON, 'r') as ff:
        response = json.load(ff)
        unfiltered_response, *__ = response['data']['children']

    print(unfiltered_response)
    filtered = redditwrapper._filter_listing(unfiltered_response)
    assert set(filtered.keys()) == set(redditwrapper.FILTERED_KEYS)

def test_game_in_listing():
    '''Check if regex search works properly.'''
    listing = {
        'title': 'cid final fantasy',
        'selftext': ''
    }

    assert redditwrapper._game_in_listing('Final Fantasy', listing)
