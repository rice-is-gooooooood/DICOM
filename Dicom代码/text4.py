import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np

# 用户输入自定义窗口中心和窗口宽度
cx = input("请输入自定义窗口中心:")
cw = input("请输入自定义窗口宽度:")


def read_dcm_image(file_path):
    """
    读取DICOM文件并返回图像数据和元数据。

    :param file_path: DICOM文件的路径
    :return: 图像像素数据和元数据
    """
    try:
        ds = pydicom.dcmread(file_path)
        image = ds.pixel_array
        return image, ds
    except Exception as e:
        print(f"读取DICOM文件时出错: {e}")
        return None, None


def normalize_image(image):
    """
    将图像像素值归一化到0到1之间。

    :param image: 要归一化的图像数据
    :return: 归一化后的图像数据
    """
    if image is not None:
        min_val = np.min(image)
        max_val = np.max(image)
        normalized_image = (image - min_val) / (max_val - min_val)
        return normalized_image
    return None


def apply_window(image, window_center, window_width):
    """
    应用窗口设置。

    :param image: 要应用窗口设置的图像数据
    :param window_center: 窗口中心
    :param window_width: 窗口宽度
    :return: 应用窗口设置后的图像数据
    """
    if image is not None:
        img_min = window_center - window_width // 2
        img_max = window_center + window_width // 2
        window_image = np.clip(image, img_min, img_max)
        window_image = (window_image - img_min) / (img_max - img_min)
        return window_image
    return None


def show_image(image, title=None):
    """
    显示图像。

    :param image: 要显示的图像数据
    :param title: 图像标题
    """
    if image is not None:
        plt.figure()
        plt.imshow(image, cmap=plt.cm.gray)
        plt.title(title)
        plt.colorbar()
        plt.show()


def display_header_info(dataset):
    """
    显示DICOM文件的头信息。

    :param dataset: 包含DICOM元数据的pydicom.Dataset对象
    """
    if dataset is not None:
        print("DICOM Header Information:")
        print(f"患者姓名: {dataset.get('PatientName', '未知')}")
        print(f"患者ID: {dataset.get('PatientID', '未知')}")
        print(f"检查日期: {dataset.get('StudyDate', '未知')}")
        print(f"模态: {dataset.get('Modality', '未知')}")
        print(f"图像尺寸: {dataset.Rows} x {dataset.Columns}")
        print(f"存储位数: {dataset.get('BitsStored', '未知')}")
        print(f"光度解释: {dataset.get('PhotometricInterpretation', '未知')}")
        print(f"像素间距: {dataset.get('PixelSpacing', '未知')}")
        print(f"窗口中心: {dataset.get('WindowCenter', '未知')}")
        print(f"窗口宽度: {dataset.get('WindowWidth', '未知')}")


def process_images_in_directory(directory_path):
    """
    处理指定目录下的所有DICOM文件。

    :param directory_path: 包含DICOM文件的目录路径
    """
    for filename in os.listdir(directory_path):
        if filename.endswith('.dcm'):
            file_path = os.path.join(directory_path, filename)
            image, dataset = read_dcm_image(file_path)

            if image is not None and dataset is not None:
                # 显示DICOM文件的头信息
                display_header_info(dataset)

                # 获取默认的窗口中心和窗口宽度
                window_center = int(dataset.get('WindowCenter', 0))
                window_width = int(dataset.get('WindowWidth', 255))

                # 应用窗口设置
                windowed_image = apply_window(image, window_center, window_width)

                # 显示应用窗口设置后的图像
                show_image(windowed_image, f"Default Windowing - {filename}")

                # 手动调整窗口中心和窗口宽度
                custom_window_center = int(cx)
                custom_window_width = int(cw)
                custom_windowed_image = apply_window(image, custom_window_center, custom_window_width)

                # 归一化图像
                normalized_image = normalize_image(custom_windowed_image)

                # 显示手动调整窗口设置后的图像
                show_image(normalized_image, f"Custom Windowing - {filename}")


if __name__ == "__main__":
    # 指定包含DICOM文件的目录路径
    dcm_directory = r'D:\RJ\Pycharm\PyCharm Community Edition 2023.3.6\pycharmproject\pythonProject1\Dicom\1.3.6.1.4.1.14519.5.2.1.6279.6001.298806137288633453246975630178\1.3.6.1.4.1.14519.5.2.1.6279.6001.179049373636438705059720603192'

    # 处理目录中的所有DICOM文件
    process_images_in_directory(dcm_directory)