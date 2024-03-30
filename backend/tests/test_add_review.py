from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_add_review():
    response = client.post('/chat/add_review',
                           json={
                               "user_name": "string",
                               "user_email": "string",
                               "user_reviews": "string",
                               "user_star_rating": 5
                           }
                           )
    assert response.status_code == 200
    assert response.json() == {"data": None, "status": "ok"}
