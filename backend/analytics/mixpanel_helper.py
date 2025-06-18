import os
from mixpanel import Mixpanel

_mp = Mixpanel(os.getenv("MIXPANEL_TOKEN"))

def record(event: str, distinct_id: str, **props):
    if _mp and _mp.token:
        _mp.track(distinct_id, event, props) 