import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np

# 设置 DICOM 文件所在的目录路径
str_path = r"D:\RJ\Pycharm\PyCharm Community Edition 2023.3.6\pycharmproject\pythonProject1\Dicom\1.3.6.1.4.1.14519.5.2.1.6279.6001.298806137288633453246975630178\1.3.6.1.4.1.14519.5.2.1.6279.6001.179049373636438705059720603192"

# 获取目录下所有 .dcm 文件
dcm_files = [f for f in os.listdir(str_path) if f.endswith('.dcm')]

# 遍历所有 DICOM 文件
for file_name in dcm_files:
    file_path = os.path.join(str_path, file_name)

    # 读取 DICOM 文件
    ds = pydicom.dcmread(file_path)

    # 获取切片位置信息
    slice_location = ds.SliceLocation
    print(f"Slice Location: {slice_location}")

    # 获取图像数据
    image = ds.pixel_array

    # 显示图像的矩阵信息
    print(f"Image Matrix Info of {file_name}:")
    print(f"Shape: {image.shape}")
    print(f"Data Type: {image.dtype}")
    print(f"Min Value: {image.min()}")
    print(f"Max Value: {image.max()}")

    # 调节窗宽窗位
    window_width = 700  # 窗宽
    window_level = -600  # 窗位
    image_rescale = (image - image.min()) * (255 / (window_width / 2)) + window_level - (window_width / 2)
    image_rescale[image_rescale < 0] = 0
    image_rescale[image_rescale > 255] = 255
    image_rescale = image_rescale.astype(np.uint8)

    # 显示调节后的图像
    plt.imshow(image_rescale, cmap='gray')
    plt.title(f"DICOM Image: {file_name}")
    plt.pause(1)  # 暂停 1 秒
    plt.close()  # 关闭图像窗口