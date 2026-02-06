import pytest

def test_this_will_fail():
    """
    This test is DESIGNED TO FAIL.
    It demonstrates what an assertion error looks like in the logs.
    """
    expected_value = "Project Chimera"
    actual_value = "Project Chaos"
    
    # This assertion will fail because the strings are different
    assert actual_value == expected_value, f"Expected '{expected_value}', but got '{actual_value}'"

def test_this_will_pass():
    """This test should pass, showing mixed results."""
    assert 1 + 1 == 2
