"""Tests to ensure that app configurations are accurate.
"""

from hybrid_orm.config import settings


def test_outpost_mode_configuration():
    if settings.OUTPOST_MODE:
        assert settings.LEADER_DB != settings.OUTPOST_DB
    else:
        assert settings.LEADER_DB == settings.OUTPOST_DB
