__author__ = "Alix Chagué"
__copyright__ = "2024 Alix Chagué"
__credits__ = ["Alix Chagué"]
__license__ = "MIT License"
__version__ = "0.0.1"

"""
After applying make_pairs.py, this script splits the dataset according to the official
partition defined for the Large Writer Independent Text Line Recognition Task.
It is described here: https://fki.tic.heia-fr.ch/databases/iam-handwriting-database"""
"""
Set Name 	    Number of Text Lines 	Number of Writers
Train 	        6'161 	                283
Validation 1 	900 	                46
Validation 2 	940 	                43
Test 	        1'861 	                128
Total 	        9'862 	                500
"""

import os
import sys
from tqdm import tqdm

path_to_files = "iam_pairs"
path_to_partition_desc = "partitions"

n_lines_at_start = len([f for f in os.listdir(path_to_files) if f.endswith(".png")])

# download the partition file from https://fki.tic.heia-fr.ch/static/zip/largeWriterIndependentTextLineRecognitionTask.zip
# and extract it in the same folder as this script under the name "partitions"
partitions_desc = {
    "trainset": os.path.join(path_to_partition_desc, "trainset.txt"),
    "validationset1": os.path.join(path_to_partition_desc, "validationset1.txt"),
    "validationset2": os.path.join(path_to_partition_desc, "validationset2.txt"),
    "testset": os.path.join(path_to_partition_desc, "testset.txt"),
}

for k in tqdm(partitions_desc, "Loading partition files"):
    if not os.path.exists(partitions_desc[k]):
        sys.exit("Path to partition description does not exist: " + partitions_desc[k])
    else:
        with open(partitions_desc[k], "r", encoding="utf8") as f:
            partitions_desc[k] = f.read().splitlines()


for k in partitions_desc:
    # create folder named after the value of k in path_to_files
    if not os.path.exists(os.path.join(path_to_files, k)):
        os.makedirs(os.path.join(path_to_files, k))
    else:
        print("Folder already exists: " + os.path.join(path_to_files, k))

    # then let's move the files in the corresponding folder
    txt_files = [os.path.join(path_to_files, f"{f}.gt.txt") for f in partitions_desc[k]]
    png_files = [os.path.join(path_to_files, f"{f}.png") for f in partitions_desc[k]]
    for f in tqdm(sorted(txt_files + png_files), f"Moving files to {k}/"):
        if not os.path.exists(f):
            print(f"File does not exist: {f}")
        else:
            os.rename(f, os.path.join(path_to_files, k, os.path.basename(f)))


# a little sanity check:
with open(os.path.join("partitions", "LargeWriterIndependentTextLineRecognitionTask.txt"), "r", encoding="utf8") as f:
    set_descs = f.read().splitlines()

total_lines_in_partitions = 0
for k in partitions_desc:
    files = os.listdir(os.path.join(path_to_files, k))
    n_img = len([f for f in files if f.endswith(".png")])
    n_txt = len([f for f in files if f.endswith(".gt.txt")])
    if n_img != len(partitions_desc[k]) or n_txt != len(partitions_desc[k]):
        print(f"Error: Something went wrong: {k} should have {len(partitions_desc[k])} files, but has {n_img} images and {n_txt} transcriptions")
    else:
        expected_n = int([s for s in set_descs if s.startswith(k)][0].split(" ")[-3])
        if n_img != expected_n:
            print(f"Error: Something went wrong: {k} should have {expected_n} files, but has {n_img} images and {n_txt} transcriptions")
        else:
            print(f"Success: {k} has {n_img} images and {n_txt} transcriptions, as expected in the official partition description!")
    total_lines_in_partitions += n_img


# let's do something with the files that were not in any partition
remaining_lines = [f for f in os.listdir(path_to_files) if f.endswith(".gt.txt")]
if len(remaining_lines) != n_lines_at_start - total_lines_in_partitions:
    print(f"Error: Something went wrong: {len(remaining_lines)} lines left, but should have {n_lines_at_start - total_lines_in_partitions}")

else:
    print(f"Success: {len(remaining_lines)} lines left, as expected!")
    print("Let's move them to a folder named 'left_out'")

    if not os.path.exists(os.path.join(path_to_files, "left_out")):
        os.makedirs(os.path.join(path_to_files, "left_out"))
    else:
        print("Folder already exists: " + os.path.join(path_to_files, "left_out"))

    # let's move the files that were not in any partition
    txt_files = [os.path.join(path_to_files, f) for f in os.listdir(path_to_files) if f.endswith(".gt.txt")]
    png_files = [os.path.join(path_to_files, f) for f in os.listdir(path_to_files) if f.endswith(".png")]

    for f in tqdm(sorted(txt_files + png_files), f"Moving remaining files to left_out/"):
        if not os.path.exists(f):
            print(f"File does not exist: {f}")
        else:
            os.rename(f, os.path.join(path_to_files, "left_out", os.path.basename(f)))

print("Done! :)")
