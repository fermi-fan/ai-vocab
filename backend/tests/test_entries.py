def create_test_entry(client) -> dict:
    """
    创建一条通用测试数据，供其他测试复用。
    """
    response = client.post(
        "/entries",
        json={
            "content": "run",
            "context": "Please run the code again.",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_entry(client):
    """
    测试正常创建条目。
    """
    response = client.post(
        "/entries",
        json={
            "content": "run",
            "context": "Please run the code again.",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["content"] == "run"
    assert data["entry_type"] == "word"
    assert data["chinese_meaning"] == "运行"
    assert data["part_of_speech"] == "verb"
    assert data["familiarity_level"] == 0

    # context 只用于 AI 判断，不允许保存或返回
    assert "context" not in data


def test_create_entry_rejects_blank_content(client):
    """
    测试 content 只有空格时会被拒绝。
    """
    response = client.post(
        "/entries",
        json={
            "content": "   ",
            "context": "Example context",
        },
    )

    assert response.status_code == 422


def test_get_entry_list(client):
    """
    测试查询条目列表。
    """
    create_response = client.post(
        "/entries",
        json={
            "content": "model",
            "context": "The model was deployed to production.",
        },
    )

    assert create_response.status_code == 201

    response = client.get("/entries")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1

    entry = data["items"][0]

    assert entry["id"] == 1
    assert entry["content"] == "model"
    assert entry["entry_type"] == "word"
    assert entry["chinese_meaning"] == "模型"

    # context 不应该出现在数据库查询结果里
    assert "context" not in entry


def test_get_existing_entry(client):
    """
    测试根据 ID 查询已经存在的条目。
    """
    created_entry = create_test_entry(client)

    entry_id = created_entry["id"]

    response = client.get(
        f"/entries/{entry_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == entry_id
    assert data["content"] == "run"
    assert data["entry_type"] == "word"
    assert data["chinese_meaning"] == "运行"
    assert data["part_of_speech"] == "verb"
    assert data["familiarity_level"] == 0

    assert "context" not in data


def test_get_nonexistent_entry(client):
    """
    测试查询不存在的条目。
    """
    response = client.get("/entries/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Entry not found",
    }


def test_update_entry_familiarity_level(client):
    """
    测试 PATCH 修改条目的熟悉度。
    """
    created_entry = create_test_entry(client)

    entry_id = created_entry["id"]

    response = client.patch(
        f"/entries/{entry_id}",
        json={
            "familiarity_level": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == entry_id

    # 原有字段不能被 PATCH 误修改
    assert data["content"] == "run"
    assert data["entry_type"] == "word"
    assert data["chinese_meaning"] == "运行"

    # 熟悉度应该被成功修改
    assert data["familiarity_level"] == 3


def test_updated_entry_can_be_queried(client):
    """
    测试 PATCH 修改后，
    数据确实已经持久化到 PostgreSQL。
    """
    created_entry = create_test_entry(client)

    entry_id = created_entry["id"]

    update_response = client.patch(
        f"/entries/{entry_id}",
        json={
            "familiarity_level": 4,
        },
    )

    assert update_response.status_code == 200

    # 再次从数据库查询
    get_response = client.get(
        f"/entries/{entry_id}"
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == entry_id
    assert data["familiarity_level"] == 4


def test_update_entry_rejects_invalid_familiarity_level(client):
    """
    测试熟悉度超过 0～5 范围时返回 422。
    """
    created_entry = create_test_entry(client)

    entry_id = created_entry["id"]

    response = client.patch(
        f"/entries/{entry_id}",
        json={
            "familiarity_level": 8,
        },
    )

    assert response.status_code == 422


def test_update_entry_rejects_empty_body(client):
    """
    测试 PATCH 没有提供任何更新字段时返回 400。
    """
    created_entry = create_test_entry(client)

    entry_id = created_entry["id"]

    response = client.patch(
        f"/entries/{entry_id}",
        json={},
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "No update fields provided",
    }


def test_update_nonexistent_entry(client):
    """
    测试修改不存在的条目时返回 404。
    """
    response = client.patch(
        "/entries/999",
        json={
            "familiarity_level": 3,
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Entry not found",
    }


def test_delete_entry(client):
    """
    测试正常删除条目。
    """
    created_entry = create_test_entry(client)

    entry_id = created_entry["id"]

    response = client.delete(
        f"/entries/{entry_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Entry deleted successfully"

    assert data["deleted"]["id"] == entry_id
    assert data["deleted"]["content"] == "run"
    assert data["deleted"]["entry_type"] == "word"


def test_deleted_entry_cannot_be_queried(client):
    """
    测试条目删除以后，
    PostgreSQL 中已经无法再次查询到该记录。
    """
    created_entry = create_test_entry(client)

    entry_id = created_entry["id"]

    delete_response = client.delete(
        f"/entries/{entry_id}"
    )

    assert delete_response.status_code == 200

    # 删除以后再次查询
    get_response = client.get(
        f"/entries/{entry_id}"
    )

    assert get_response.status_code == 404

    assert get_response.json() == {
        "detail": "Entry not found",
    }


def test_delete_nonexistent_entry(client):
    """
    测试删除不存在的条目时返回 404。
    """
    response = client.delete(
        "/entries/999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Entry not found",
    }