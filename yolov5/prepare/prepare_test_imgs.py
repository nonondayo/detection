import os
import tqdm
import shutil


if __name__ == "__main__":
    test_txt_path = os.path.join("../datasets/RDD2022/test.txt")
    with open("test_data.txt", "r") as reader:
        test_datasets = reader.readlines()
    test_datasets = [one.strip() for one in test_datasets]
    target_path = os.path.join("../datasets/RDD2022/testimgs")
    if os.path.exists(target_path):
        print(f"delete {target_path}")
        shutil.rmtree(target_path)
        os.makedirs(target_path)
    else:
        os.makedirs(target_path)

    # move test images
    test_images_paths = []
    for dataset in test_datasets:
        test_path = os.path.join("../datasets/RDD2022", dataset, "test/images")
        assert os.path.exists(test_path), f"{test_path} not exists!"
        progress_bar = tqdm.tqdm(desc=f"move test images of {dataset}", total=len(os.listdir(test_path)))
        for imgname in os.listdir(test_path):
            shutil.copy(os.path.join(test_path, imgname), os.path.join(target_path, imgname))
            progress_bar.update()
        progress_bar.close()

