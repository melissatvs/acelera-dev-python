from main import get_temperature
import pytest
from unittest.mock import patch


values = [
    (-14.235004, -51.92528, 62, 16),
    (-22.932924, -47.073845, 53, 11),
    (41.781200, 12.385230, 70, 21)
]

@pytest.mark.parametrize('lat,lng,temperature,expected', values)
def test_get_temperature_by_lat_lng(lat, lng, temperature, expected):
    expected_result = {
        'currently': {
            'temperature': temperature
        }
    }
    mock_requests = patch('main.requests.get')
    
    get = mock_requests.start()
    
    get.return_value.json.return_value = expected_result
    
    result = get_temperature(lat, lng)
    
    mock_requests.stop()
    
    assert result == expected
