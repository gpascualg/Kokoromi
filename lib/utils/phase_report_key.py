from typing import Dict
from pytest import StashKey, CollectReport

phase_report_key = StashKey[Dict[str, CollectReport]]()
