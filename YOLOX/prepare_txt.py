import os


if __name__ == "__main__":
    train_txt_path = os.path.join("datasets/RDD2022/ImageSets/Main/train.txt")
    val_txt_path = os.path.join("datasets/RDD2022/ImageSets/Main/val.txt")
    datapath = os.path.join("datasets/RDD2022/JPEGImages")
    train_images_paths = []
    for imgname in os.listdir(datapath):
        imgname = imgname.split(".")[0]
        train_images_paths.append(imgname)
    val_images_paths = train_images_paths[-9:]
    with open(train_txt_path, "w") as file:
        for img in train_images_paths:
            file.write(img + "\n")
    with open(val_txt_path, "w") as file:
        for img in val_images_paths:
            file.write(img + "\n")
            