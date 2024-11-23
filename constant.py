from typing import Union
from block import *

PROPERTY_BLCOK = Union[StreetBlock, RailroadBlock, UtilityBlock]
TAX_BLOCK = Union[IncomeTaxBlock, LuxuryTaxBlock]
EVENT_BLOCK = Union[CommunityChestBlock, ChanceBlock]
CORNER_BLOCK = Union[StartBlock, ImprisonBlock, InJailOrJustVisitingBlock, FreeParkingBlock]
BLOCK = Union[PROPERTY_BLCOK, TAX_BLOCK, EVENT_BLOCK, CORNER_BLOCK]