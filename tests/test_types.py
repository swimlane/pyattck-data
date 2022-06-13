# -*- coding: utf-8 -*-
import pytest


from pyattck_data.types import (
    Id,
    MitreDomain,
    MitrePlatform,
    PATTERNS,
    SemVersion
)


def test_id_type():
    for example in PATTERNS["types"]["examples"]:
        assert Id().validate(example)

    with pytest.raises(ValueError) as excinfo:
        Id().validate('asdefasdf')
    assert "Invalid Id attribute" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Id().validate('asdefasdf-')
    assert "Invalid Id attribute" in str(excinfo.value)


def test_semversion_type():
    for example in PATTERNS["semversion"]["examples"]:
        assert SemVersion().validate(example)

    with pytest.raises(ValueError) as excinfo:
        SemVersion().validate('asdefasdf')
    assert "Invalid SemVersion format" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        SemVersion().validate('0000')
    assert "Invalid SemVersion format" in str(excinfo.value)


def test_mitre_domain_type():
    for example in PATTERNS["domains"]["examples"]:
        assert MitreDomain().validate(example)

    with pytest.raises(ValueError) as excinfo:
        MitreDomain().validate('asdefasdf')
    assert "Invalid MitreDomain attribute" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        MitreDomain().validate('0000')
    assert "Invalid MitreDomain attribute" in str(excinfo.value)


def test_mitre_platform_type():
    for example in PATTERNS["platforms"]["examples"]:
        assert MitrePlatform().validate(example)

    with pytest.raises(ValueError) as excinfo:
        MitrePlatform().validate('android')
    assert "Invalid MitrePlatform attribute" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        MitrePlatform().validate('relationship')
    assert "Invalid MitrePlatform attribute" in str(excinfo.value)
