import uuid

from common_helpers.uuid_helper import UuidHelper

def test_uuid_round_trip():
    """
    Test that a UUID can be converted to a string and back to a UUID
    """
    original_uuid = uuid.uuid4()
    assert UuidHelper.is_valid_uuid(str(original_uuid)) is True
    
    uuid_str = UuidHelper.from_uuid(original_uuid)
    assert UuidHelper.is_valid_uuid(uuid_str) is True
    
    converted_uuid = UuidHelper.to_uuid(uuid_str)
    assert original_uuid == converted_uuid