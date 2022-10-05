import os
import xml.etree.ElementTree as ET
import tqdm
import shutil


def makedir(newdir):
    if not os.path.exists(newdir):
        os.makedirs(newdir)


def onexml2yolo(xmlpath, classname):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    size = root.find("size")
    width = int(float(size.find("width").text))
    height = int(float(size.find("height").text))
    newlines = []
    for oneobject in root.findall("object"):
        bndbox = oneobject.find("bndbox")
        name = oneobject.find("name").text
        xmin = int(float(bndbox.find("xmin").text))
        ymin = int(float(bndbox.find("ymin").text))
        xmax = int(float(bndbox.find("xmax").text))
        ymax = int(float(bndbox.find("ymax").text))
        xcenter = (xmax + xmin) / (2. * width)
        ycenter = (ymax + ymin) / (2. * height)
        yolowidth = (xmax - xmin) / width
        yoloheight = (ymax - ymin) / height
        if name not in classname.keys():
            continue
        line = f"{classname[name]} " + f"{xcenter:.6f} {ycenter:.6f} {yolowidth:.6f} {yoloheight:.6f}"
        newlines.append(line)
    return newlines


def generate_yolo_label(xmlpath, outpath, classname, dataname):
    makedir(outpath)
    progress_bar = tqdm.tqdm(desc=f"{dataname} xml2yolo", total=len(os.listdir(xmlpath)))
    for xml in os.listdir(xmlpath):
        newname = xml.split(".")[0]
        newname = newname + ".txt"
        xml = os.path.join(xmlpath, xml)
        newlines = onexml2yolo(xml, classname)
        with open(os.path.join(outpath, newname), "w") as f:
            for line in newlines:
                f.write(line + "\n")
        progress_bar.update()
    progress_bar.close()


def delete_cache(path):
    for filename in os.listdir(path):
        if filename.endswith(".cache"):
            os.remove(os.path.join(path, filename))


if __name__ == "__main__":
    classname = {"D00": 0, "D10": 1, "D20": 2, "D40": 3}
    train_txt_path = os.path.join("../datasets/RDD2022/train.txt")
    val_txt_path = os.path.join("../datasets/RDD2022/val.txt")
    test_txt_path = os.path.join("../datasets/RDD2022/test.txt")
    delete_cache(os.path.join("../datasets/RDD2022"))

    with open("train_data.txt", "r") as reader:
        train_datasets = reader.readlines()
    train_datasets = [one.strip() for one in train_datasets]
    with open("test_data.txt", "r") as reader:
        test_datasets = reader.readlines()
    test_datasets = [one.strip() for one in test_datasets]

    # create train.txt val.txt
    train_images_paths = []
    val_images_paths = []
    for dataset in train_datasets:
        datapath = os.path.join("../datasets/RDD2022", dataset)
        assert os.path.exists(datapath), f"{datapath} not exists!"

        uppath = "datasets/RDD2022/" + dataset + "/train/images"
        xmls_path = os.path.join(datapath, "train/annotations/xmls")
        output_path = os.path.join(datapath, "train/labels")
        makedir(output_path)
        # xml to yolo
        generate_yolo_label(xmls_path, output_path, classname, dataset)
        # train.txt
        for imgname in os.listdir(os.path.join(datapath, "train/images")):
            train_images_paths.append(uppath + f"/{imgname}")
        val_images_paths.extend(train_images_paths[-3:])
    with open(train_txt_path, "w") as file:
        for img in train_images_paths:
            file.write(img + "\n")
    with open(val_txt_path, "w") as file:
        for img in val_images_paths:
            file.write(img + "\n")

    # create test.txt
    test_images_paths = []
    for dataset in test_datasets:
        test_path = os.path.join("../datasets/RDD2022", dataset, "test/images")
        assert os.path.exists(test_path), f"{test_path} not exists!"
        uppath = "datasets/RDD2022/" + dataset + "/test/images"
        for imgname in os.listdir(test_path):
            test_images_paths.append(uppath+f"/{imgname}")
    with open(test_txt_path, "w") as file:
        for img in test_images_paths:
            file.write(img + "\n")

