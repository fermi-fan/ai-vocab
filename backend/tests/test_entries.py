import pytest
from fastapi.testclient import TestClient

from entry_store import reset_entry_store
from main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_entry_store():
    """
    每个测试执行前后都清空内存数据，
    确保不同测试之间不会互相影响。
    """
    reset_entry_store()

    yield

    reset_entry_store()


def create_test_entry() -> dict:
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


def test_create_entry():
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

    # context 只用于 AI 判断，不应该保存或返回
    assert "context" not in data


def test_create_entry_rejects_blank_content():
    """
    测试只有空格的 content 会被拒绝。
    """
    response = client.post(
        "/entries",
        json={
            "content": "   ",
            "context": "Example context",
        },
    )

    assert response.status_code == 422


def test_get_entry_list():
    """
    测试查询条目列表。
    """
    client.post(
        "/entries",
        json={
            "content": "model",
            "context": "The model was deployed to production.",
        },
    )

    response = client.get("/entries")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == 1
    assert data["items"][0]["content"] == "model"
    assert data["items"][0]["entry_type"] == "word"
    assert data["items"][0]["chinese_meaning"] == "模型"


def test_get_existing_entry():
    """
    测试根据 ID 查询已经存在的条目。
    """
    created_entry = create_test_entry()
    entry_id = created_entry["id"]

    response = client.get(f"/entries/{entry_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == entry_id
    assert data["content"] == "run"
    assert data["entry_type"] == "word"
    assert data["chinese_meaning"] == "运行"
    assert data["familiarity_level"] == 0


def test_get_nonexistent_entry():
    """
    测试查询不存在的条目。
    """
    response = client.get("/entries/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Entry not found",
    }


def test_update_entry_familiarity_level():
    """
    测试 PATCH 修改条目的熟悉度。
    """
    created_entry = create_test_entry()
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
    assert data["content"] == "run"
    assert data["chinese_meaning"] == "运行"
    assert data["familiarity_level"] == 3


def test_updated_entry_can_be_queried():
    """
    测试修改后的数据确实已经保存到内存中。
    """
    created_entry = create_test_entry()
    entry_id = created_entry["id"]

    update_response = client.patch(
        f"/entries/{entry_id}",
        json={
            "familiarity_level": 4,
        },
    )

    assert update_response.status_code == 200

    get_response = client.get(f"/entries/{entry_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == entry_id
    assert data["familiarity_level"] == 4


def test_update_entry_rejects_invalid_familiarity_level():
    """
    测试熟悉度超过允许范围时返回 422。
    """
    created_entry = create_test_entry()
    entry_id = created_entry["id"]

    response = client.patch(
        f"/entries/{entry_id}",
        json={
            "familiarity_level": 8,
        },
    )

    assert response.status_code == 422


def test_update_entry_rejects_empty_body():
    """
    测试 PATCH 请求没有提交任何修改字段时返回 400。
    """
    created_entry = create_test_entry()
    entry_id = created_entry["id"]

    response = client.patch(
        f"/entries/{entry_id}",
        json={},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "No update fields provided",
    }


def test_update_nonexistent_entry():
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


def test_delete_entry():
    """
    测试正常删除条目。
    """
    created_entry = create_test_entry()
    entry_id = created_entry["id"]

    response = client.delete(f"/entries/{entry_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Entry deleted successfully"
    assert data["deleted"]["id"] == entry_id
    assert data["deleted"]["content"] == "run"


def test_deleted_entry_cannot_be_queried():
    """
    测试条目删除后无法再查询。
    """
    created_entry = create_test_entry()
    entry_id = created_entry["id"]

    delete_response = client.delete(f"/entries/{entry_id}")

    assert delete_response.status_code == 200

    get_response = client.get(f"/entries/{entry_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Entry not found",
    }


def test_delete_nonexistent_entry():
    """
    测试删除不存在的条目时返回 404。
    """
    response = client.delete("/entries/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Entry not found",
    }