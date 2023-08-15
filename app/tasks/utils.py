import os


def count_files_in_folder(folder_path: str) -> int:
    files = os.listdir(folder_path)
    files = list(filter(lambda file: file.endswith(".webp"), files))
    return len(files)


def save_file_to_disk(file_name: str, file) -> str:
    folder_path = "./app/static/tmp"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(f"{folder_path}/{file_name}", "wb") as f:
        f.write(file.read())
        return f.name


def remove_file_from_disk(file_path: str):
    os.remove(file_path)
