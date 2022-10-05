import cv2
import os
import shutil
import xml.etree.ElementTree as ET
import tqdm


def makedir(newdir):
    if not os.path.exists(newdir):
        os.makedirs(newdir)


def resizexml(xmlpath, newimgsize, outputpath):
    xmlname = os.path.basename(xmlpath)
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)
    for oneobject in root.findall("object"):
        bndbox = oneobject.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)
        bndbox.find("xmin").text = str(int(xmin/width*newimgsize))
        bndbox.find("ymin").text = str(int(ymin/height*newimgsize))
        bndbox.find("xmax").text = str(int(xmax/width*newimgsize))
        bndbox.find("ymax").text = str(int(ymax/height*newimgsize))
    root.find("size").find("width").text = str(newimgsize)
    root.find("size").find("height").text = str(newimgsize)
    tree.write(os.path.join(outputpath, xmlname))


if __name__ == '__main__':
    origin_path = os.path.join("D:/CRDDC2022/yolov5-6.0/datasets/RDD2022/Norway/train/images")
    output_path = os.path.join("D:/CRDDC2022/yolov5-6.0/datasets/RDD2022/Norway_resize")
    test_path = os.path.join("D:/CRDDC2022/yolov5-6.0/datasets/RDD2022/Norway/test/images")
    imgsize = 640

    makedir(output_path)
    resize_images_path = os.path.join(output_path, "train/images")
    resize_xmls_path = os.path.join(output_path, "train/annotations/xmls")
    test_images_path = os.path.join(output_path, "test/images")
    makedir(resize_images_path)
    makedir(resize_xmls_path)
    makedir(test_images_path)

    # resize training images
    progress_bar1 = tqdm.tqdm(desc=f"resize training images", total=len(os.listdir(origin_path)))
    for imgname in os.listdir(origin_path):
        img = cv2.imread(os.path.join(origin_path, imgname))
        img = cv2.resize(img, (int(imgsize), int(imgsize)))
        cv2.imwrite(os.path.join(resize_images_path, imgname), img)
        xml = os.path.join(os.path.split(origin_path)[0], "annotations/xmls", imgname.split(".")[0]+".xml")
        resizexml(xml, imgsize, resize_xmls_path)
        progress_bar1.update()
    progress_bar1.close()

    # copy testing images
    progress_bar2 = tqdm.tqdm(desc=f"copy testing images", total=len(os.listdir(test_path)))
    for imgname in os.listdir(test_path):
        shutil.copy(os.path.join(test_path, imgname), os.path.join(test_images_path, imgname))
        progress_bar2.update()
    progress_bar2.close()
