from cx_Freeze import setup, Executable
import os

# Путь к ресурсам
resource_folders = ['fonts', 'settings', 'sound', 'sprites']

def collect_files(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

# Сбор всех файлов из папок ресурсов
include_files = []
for folder in resource_folders:
    include_files.extend(collect_files(folder))

build_exe_options = {
    "packages": ["pygame", "json", "sys", "os", "time", "random", "math"],  # Пакеты для включения
    "include_files": include_files
}

setup(
    name="CoconutCoin",
    version="0.1",
    description="CoconutCoin Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("menu.py", base=None)]  # Основной файл
)
