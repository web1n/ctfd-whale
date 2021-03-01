from tests.helpers import create_ctfd, destroy_ctfd, register_user, login_as_user
from CTFd.utils import set_config
from requests import session

import time

challenge_data = {
    "name": "name",
    "category": "category",
    "description": "description",
    "value": 100,
    "initial": 100,
    "decay": 10,
    "minimum": 50,
    "state": "hidden",
    "type": "dynamic_docker",

    "docker_image": "nginx",
    "redirect_type": "http",
    "redirect_port": 80,
}


def test_create_whale_challenge():
    """Test that an admin can create a challenge properly"""
    app = create_ctfd(enable_plugins=True)
    with app.app_context():
        register_user(app)
        client = login_as_user(app, name="admin", password="password")

        r = client.post("/api/v1/challenges", json=challenge_data)
        assert r.get_json().get("data")["id"] == 1
        r = client.get("/admin/challenges/1")
        assert r.status_code == 200
        r = client.get("/api/v1/challenges/1")
        assert r.get_json().get("data")["id"] == 1

    destroy_ctfd(app)


def test_create_whale_container():
    app = create_ctfd(enable_plugins=True)
    with app.app_context():
        set_config("whale:frp_api_url", "http://frpc:7400")
        set_config("whale:docker_auto_connect_network", "ctfd-whale_default")
        register_user(app)
        client = login_as_user(app, name="admin", password="password")

        r = client.post("/api/v1/challenges", json=challenge_data)
        assert r.get_json().get("data")["id"] == 1
        assert client.post("/api/v1/plugins/ctfd-whale/container?challenge_id=1", json={
        }).get_json()["success"]

        r = client.get("/api/v1/plugins/ctfd-whale/container?challenge_id=1")
        access = r.get_json()['data']['user_access']
        ses = session()
        cnt = 5
        while cnt:
            r = ses.get(
                'http://frps:8080',
                headers={'Host': access.lstrip('http://').rstrip('/')}
            ).text
            if 'Welcome to nginx!' in r:
                break
            time.sleep(3)
            cnt -= 1
        assert 'Welcome to nginx!' in r

    destroy_ctfd(app)
