import glob
import os
import allure

from PIL import Image, ImageChops

from settings import ROOT_DIR

@allure.step('Обрезка изображения по 2 точкам')
def crop_image(path_image:str, path_new_image:str, points:tuple):
    """функция для обрезки изображения по 2 точкам (4 значения, x1,y1,x2,y2)"""
    img = Image.open(path_image)
    crop_image = img.crop(points)
    crop_image.save(path_new_image)


@allure.step('Сравнение 2 изображений')
def are_images_equal(image_path1, image_path2):
    """сравнения изображений"""
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    difference = ImageChops.difference(img1, img2)

    if not difference.getbbox():
        return True
    else:
        return False


@allure.step('Наличие файлов с форматом {format_file}')
def are_files_in_dir(list_dir_name: tuple, format_file:str ='png'):
    files = glob.glob(os.path.join(ROOT_DIR, *list_dir_name,f'*.{format_file}'))
    if files:
        return True
    return False


@allure.step('Удаление файлов по формату {format_file}')
def delete_files_in_dir(list_dir_name:tuple, format_file: str):
    files = glob.glob(os.path.join(ROOT_DIR, *list_dir_name,f'*.{format_file}'))
    for file in files:
        os.remove(file)
