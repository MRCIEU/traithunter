# from starlette.testclient import TestClient

# from app.main import app


# def test_graphql_query_user():
#     query = """query {
#         user {
#           name
#           age
#         }
#     }
#     """
#     payload = {"query": query}
#     with TestClient(app) as client:
#         r = client.post("/graphql", json=payload)
#     print(r.json())
#     assert r.ok
