def test_create_task_successfully(client):
    task = {
        "name": "test task",
        "description": "test desc"
    }

    expected = {
        "name": "test task",
        "description": "test desc",
        "status": "PENDING"
    }

    response = client.post("/tasks", json=task)
    task_id = response.json().get("id")

    expected["id"] = task_id

    assert response.status_code == 201
    assert response.json() == expected


def test_list_all_tasks(client):
    expected = {
        "name": "test task",
        "description": "test desc",
        "status": "PENDING"
    }

    response = client.get("/tasks")
    result = response.json()

    assert response.status_code == 200

    for task in result:
        del task["id"]

    assert expected in result


def test_get_task_by_id(client):
    expected = {
        "name": "test task",
        "description": "test desc",
        "status": "PENDING"
    }

    tasks_response = client.get("/tasks")
    response = client.get(f"/tasks/{tasks_response.json()[0]['id']}")

    assert tasks_response.status_code == 200
    assert response.status_code == 200

    result = response.json()
    del result["id"]

    assert result == expected


def test_update_task(client):
    expected = {
        "name": "test task",
        "description": "test desc",
        "status": "IN_PROGRESS"
    }

    payload = {"status": "IN_PROGRESS"}

    tasks_response = client.get("/tasks")
    response = client.patch(
        f"/tasks/{tasks_response.json()[0]['id']}",
        json=payload
    )

    assert tasks_response.status_code == 200
    assert response.status_code == 200

    result = response.json()
    del result["id"]

    assert result == expected


def test_delete_task(client):
    tasks_response = client.get("/tasks")
    response = client.delete(f"/tasks/{tasks_response.json()[0]['id']}")

    assert tasks_response.status_code == 200
    assert response.status_code == 204

    final_response = client.get("/tasks")

    assert final_response.status_code == 200
    assert final_response.json() == []


def test_get_non_existing_task(client):
    expected = {"detail": "Task 123 not found."}

    response = client.get(f"/tasks/123")

    assert response.status_code == 404
    assert response.json() == expected


def test_create_task_missing_required_fields(client):
    task = {"description": "test desc"}

    expected = {
        "detail": [
            {
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }

    response = client.post("/tasks", json=task)

    assert response.status_code == 422
    assert response.json() == expected


def test_update_non_existing_task(client):
    expected = {"detail": "Task 123 not found."}
    payload = {"name": "test name"}

    response = client.patch(f"/tasks/123", json=payload)

    assert response.status_code == 404
    assert response.json() == expected


def test_update_task_to_unpermitted_status(client):
    expected = {
        "detail": [
            {
                "loc": [
                    "body",
                    "status"
                ],
                "msg": "value is not a valid enumeration member; permitted: 'DONE', 'PENDING', 'IN_PROGRESS'",
                "type": "type_error.enum",
                "ctx": {
                    "enum_values": [
                        "DONE",
                        "PENDING",
                        "IN_PROGRESS"
                    ]
                }
            }
        ]
    }

    payload = {"status": "JUST_DO_IT"}

    response = client.patch("/tasks/123", json=payload)

    assert response.status_code == 422
    assert response.json() == expected


def test_delete_non_existing_task(client):
    expected = {"detail": "Task 123 not found."}

    response = client.get(f"/tasks/123")

    assert response.status_code == 404
    assert response.json() == expected
