class TestStatusResponse:
    def test_index_response(self, client):
        response = client.get("/")

        assert response.status_code == 200

    def test_tools_list_response(self, client):
        response = client.get("/tools")

        assert response.status_code == 200