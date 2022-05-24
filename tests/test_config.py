import pytest

from sync.config import Config

VALID_CONFIG = {
    "DATABASE_DSN": "postgresql://",
    "DATABASE_TABLE": "contacts",
    "RAPIDPRO_HOST": "textit.in",
    "RAPIDPRO_TOKEN": "b50c919959954e5a8c5476c2b9d671e2",
    "CONCURRENCY": "5",
    "URN_TYPE": "whatsapp",
}


def test_config_valid():
    config = Config.from_environment(VALID_CONFIG)
    assert config.database_dsn == "postgresql://"
    assert config.database_table == "contacts"
    assert config.rapidpro_host == "textit.in"
    assert config.rapidpro_token == "b50c919959954e5a8c5476c2b9d671e2"
    assert config.concurrency == 5
    assert config.urn_type == "whatsapp"


def test_missing_value():
    c = VALID_CONFIG.copy()
    c.pop("DATABASE_DSN")
    with pytest.raises(KeyError) as e_type:
        Config.from_environment(c)
    assert (
        e_type.value.args[0] == "Cannot find required environment variable DATABASE_DSN"
    )


def test_invalid_type():
    c = VALID_CONFIG.copy()
    c["CONCURRENCY"] = "invalid"
    with pytest.raises(ValueError) as e_type:
        Config.from_environment(c)
    assert e_type.value.args[0] == "CONCURRENCY environment variable is not an integer"
