import global_data
import os
from pathlib import Path

print("Путь к файлу существует, файл существует: ")
filename = "C:\\Users\\Татьяна Калашникова\\CODE\\NOTES_APPLICATION\\test.csv"
print(filename + ":\n")

print("os.path.exists(filename) => {}".format(os.path.exists(filename)))
print("os.path.exists(Path(filename)) => {}".format(os.path.exists(Path(filename))))
print("os.path.isfile(filename) => {}".format(os.path.isfile(filename)))
print("os.path.isfile(Path(filename)) => {}".format(os.path.isfile(Path(filename))))
print("os.path.dirname(Path(filename)) => {}".format(os.path.dirname(Path(filename))))
print("os.path.isfile(os.path.dirname(Path(filename))) => {}".format(os.path.isfile(os.path.dirname(Path(filename)))))
print("os.path.isdir(os.path.dirname(Path(filename))) => {}".format(os.path.isdir(os.path.dirname(Path(filename)))))
print("os.path.splitext(filename) => {}".format(os.path.splitext(filename)))
print("os.path.splitext(Path(filename)) => {}".format(os.path.splitext(Path(filename))))
print("os.path.basename(filename) => {}".format(os.path.basename(filename)))

print("\nПуть к файлу существует, файла не существует: \n")
filename = "C:\\Users\\Татьяна Калашникова\\CODE\\NOTES_APPLICATION\\test1.csv"
print(filename + ":\n")

print("os.path.exists(filename) => {}".format(os.path.exists(filename)))
print("os.path.exists(Path(filename)) => {}".format(os.path.exists(Path(filename))))
print("os.path.isfile(filename) => {}".format(os.path.isfile(filename)))
print("os.path.isfile(Path(filename)) => {}".format(os.path.isfile(Path(filename))))
print("os.path.dirname(Path(filename)) => {}".format(os.path.dirname(Path(filename))))
print("os.path.isfile(os.path.dirname(Path(filename))) => {}".format(os.path.isfile(os.path.dirname(Path(filename)))))
print("os.path.isdir(os.path.dirname(Path(filename))) => {}".format(os.path.isdir(os.path.dirname(Path(filename)))))
print("os.path.splitext(filename) => {}".format(os.path.splitext(filename)))
print("os.path.splitext(Path(filename)) => {}".format(os.path.splitext(Path(filename))))
print("os.path.basename(filename) => {}".format(os.path.basename(filename)))

print("\nБерем файл из текущего каталога: \n")
filename = "test.csv"
print(filename + ":\n")

print("os.path.exists(filename) => {}".format(os.path.exists(filename)))
print("os.path.exists(Path(filename)) => {}".format(os.path.exists(Path(filename))))
print("os.path.isfile(filename) => {}".format(os.path.isfile(filename)))
print("os.path.isfile(Path(filename)) => {}".format(os.path.isfile(Path(filename))))
print("os.path.dirname(Path(filename)) => {}".format(os.path.dirname(Path(filename))))
print("os.path.isfile(os.path.dirname(Path(filename))) => {}".format(os.path.isfile(os.path.dirname(Path(filename)))))
print("os.path.isdir(os.path.dirname(Path(filename))) => {}".format(os.path.isdir(os.path.dirname(Path(filename)))))
print("os.path.splitext(filename) => {}".format(os.path.splitext(filename)))
print("os.path.splitext(Path(filename)) => {}".format(os.path.splitext(Path(filename))))
print("os.path.basename(filename) => {}".format(os.path.basename(filename)))

print("\nБерем файл из выше лежащего каталога: \n")
filename = "..\\lotteryResult.txt"
print(filename + ":\n")

print("os.path.exists(filename) => {}".format(os.path.exists(filename)))
print("os.path.exists(Path(filename)) => {}".format(os.path.exists(Path(filename))))
print("os.path.isfile(filename) => {}".format(os.path.isfile(filename)))
print("os.path.isfile(Path(filename)) => {}".format(os.path.isfile(Path(filename))))
print("os.path.dirname(Path(filename)) => {}".format(os.path.dirname(Path(filename))))
print("os.path.isfile(os.path.dirname(Path(filename))) => {}".format(os.path.isfile(os.path.dirname(Path(filename)))))
print("os.path.isdir(os.path.dirname(Path(filename))) => {}".format(os.path.isdir(os.path.dirname(Path(filename)))))
print("os.path.splitext(filename) => {}".format(os.path.splitext(filename)))
print("os.path.splitext(Path(filename)) => {}".format(os.path.splitext(Path(filename))))
print("os.path.basename(filename) => {}".format(os.path.basename(filename)))

current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file)

path_name = os.path.dirname(Path("test.csv"))
print("test.csv")
print(os.path.dirname(Path("test.csv")) == '')
print(path_name)
print(path_name == '')

path_name = os.path.dirname(Path(".\\test.csv"))
print(".\\test.csv")
print(path_name)
print(path_name == '')

path_name = os.path.dirname(Path("..\\test.csv"))
print("..\\test.csv")
print(path_name)
print(path_name == '..')
