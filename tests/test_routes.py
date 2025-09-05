from unittest.mock import patch
from app import start_time, readiness_time


def test_get_ip(client):
    """
    Test the '/' route to ensure it returns the default remote address
    when no proxy headers are present.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {'ip': '127.0.0.1'}


def test_get_ip_with_x_forwarded_for(client):
    """
    Test the '/' route to ensure it correctly parses the IP address
    from the 'X-Forwarded-For' header.
    """
    headers = {
        'X-Forwarded-For': '192.168.1.1, 10.0.0.1'
    }
    response = client.get('/', headers=headers)
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {'ip': '192.168.1.1'}


def test_health_check(client):
    with patch('time.time', return_value=start_time + readiness_time - 0.1):
        response_not_ready = client.get('/health')
        assert response_not_ready.status_code == 200
        assert response_not_ready.is_json
        assert response_not_ready.get_json() == {'status': 'not_ready'}

    with patch('time.time', return_value=start_time + readiness_time):
        response_ready = client.get('/health')
        assert response_ready.status_code == 200
        assert response_ready.is_json
        assert response_ready.get_json() == {'status': 'healthy'}


def test_readiness_probe_flow(client):
    with patch('time.time', return_value=start_time + readiness_time - 0.1):
        response_not_ready = client.get('/ready')
        assert response_not_ready.status_code == 200
        assert response_not_ready.is_json
        assert response_not_ready.get_json() == {'status': 'not_ready'}

    with patch('time.time', return_value=start_time + readiness_time):
        response_ready = client.get('/ready')
        assert response_ready.status_code == 200
        assert response_ready.is_json
        assert response_ready.get_json() == {'status': 'ready'}
