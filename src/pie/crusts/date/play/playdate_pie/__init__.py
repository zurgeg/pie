PIE_NAME = "Playdate Piecrust"
PIE_PKG_DESCRIPTION = "Unofficial piecrusts for Playdate"
PIE_AUTHOR = "zurgeg"

from . import playdate

PIE_PROVIDES = {"playdate": playdate}
PIE_LANGUAGES = {"playdate": ["lua", "c"]}