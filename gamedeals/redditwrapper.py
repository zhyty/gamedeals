'''Provide wrapper functions around Reddit API functionality.

Functions assume standard r/GameDeals format (i.e. games in title or in post).

.. note:: "listing"

   In general, "listing" refers to the object post-filtration

'''
import re
import requests

FILTERED_KEYS = [
    'kind',
    'domain',
    'title',
    'score',
    'name',
    'subreddit_id',
    'permalink',
    'selftext'
]

def _filter_listing(listing):
    '''Take a reddit API listing object and filter it to the bare minimum.
    
    :returns:
    a filtered listings object only containing the keys in `FILTERED_KEYS`.
    
    '''
    # some keys are in the data inner object, some outside
    filtered = {key: listing['data'][key] 
                for key in listing['data'] if key in FILTERED_KEYS}
    filtered['kind'] = listing['kind']
    return filtered

def _game_in_listing(game, listing):
    '''Look for occurrences of `game` in `listing`.

    Specifically checks the listing's title and selftext.

    .. note::

       Currently unable to handle cases where a title says something like 'No
       Final Fantasy'.

    '''
    title_match = re.match('.*{}.*'.format(re.escape(game)),
                           listing['title'],
                           re.IGNORECASE)
    text_match = re.match('.*{}.*'.format(re.escape(game)),
                          listing['selftext'],
                          re.IGNORECASE)
    return title_match is not None or text_match is not None

def get_deals():
    '''Retrieve new deals from reddit API.

    :returns: list of (filtered) listings objects.
    
    '''
    response = requests.get('https://www.reddit.com/r/GameDeals/new.json').json()
    listings = response['data']['children']
    return {_filter_listing(l) for l in listings}
