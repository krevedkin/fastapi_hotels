import os

import pytest
from httpx import AsyncClient

from app.tasks.utils import count_files_in_folder, remove_file_from_disk


@pytest.mark.images
async def test_resize_image_to_webp(auth_ac: AsyncClient):
    with open("./tests/mock_data/Rickroll.jpg", "rb") as f:
        response = await auth_ac.post(
            "/images/resize", files={"file": f}, params={"folder_to_save": "hotels"}
        )
        assert response.status_code == 200

        expected_file_path = "app/static/images/hotels/"
        files_count = count_files_in_folder(expected_file_path)

        new_file = f"{expected_file_path}/{files_count + 1}.webp"

        while not os.path.exists(new_file):
            print("waiting for task finish...")

        assert os.path.exists(new_file) is True
        remove_file_from_disk(new_file)
        assert os.path.exists(new_file) is False
