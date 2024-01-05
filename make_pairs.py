__author__ = "Alix Chagué"
__copyright__ = "2024 Alix Chagué"
__credits__ = ["Alix Chagué"]
__license__ = "MIT License"
__version__ = "0.0.1"

"""
A parser to create pairs of TXT + PNG to train Kraken models on IAM Db
"""

import os
import sys
import lxml.etree as ET
from tqdm import tqdm

# lines.tgz and xml.tgz can be downloaded from http://www.fki.inf.unibe.ch/databases/iam-handwriting-database/download-the-iam-handwriting-database
# lines.tgz should have been extracted in the same folder as this script under the name "lines"
# xml.tgz should have been extracted in the same folder as this script under the name "xml"
path_to_line_images = "lines"
path_to_xml = "xml"
output_folder = "iam_pairs" # where to store the pairs of TXT + PNG

# Check if the paths to the line images and to the xml files exist
if not os.path.exists(path_to_line_images):
    sys.exit("Path to image lines does not exist: " + path_to_line_images)
if not os.path.exists(path_to_xml):
    sys.exit("Path to xml files does not exist: " + path_to_xml)

# Check if the output folder exists
#if not os.path.exists(output_folder):
#    os.makedirs(output_folder)
#else:
#    print("Output folder already exists: " + output_folder)


# let's open each xml files in the xml folder
# then we want to get each "line" node, the value of the @id attribute and the value of the @text attribute
    
print("Step 1/2 Parsing XML files and extracting transcriptions")
transcriptions = {}

for root, dirs, files in tqdm(os.walk(path_to_xml)):
    for file in files:
        #print("Opening " + file)
        xml_file = os.path.join(path_to_xml, file)
        root = ET.parse(xml_file).getroot()
        # get the value of the @id attribute of the "line" node
        for line in root.iter("line"):
            if line.get("id") and line.get("text"):
                transcriptions[line.get("id")] = line.get("text")
            else:
                print(f"In {file}, no id or text for line: {line.get('id')}")

print("Step 2/2 Matching transcription with images, copying PNG files and creating TXT files")
for root, dirs, files in tqdm(os.walk(path_to_line_images)):
    for file in files:
        # {extract_id}/{writer_id}/{extract_id}-{writer_id}-{line_id}.png
        extract_id = file.split("-")[0]
        writer_id = file.split("-")[1]
        line_id = file.split("-")[2].split(".")[0]
        path_to_png = os.path.join(path_to_line_images, extract_id, f"{extract_id}-{writer_id}", f"{extract_id}-{writer_id}-{line_id}.png")
        
        transcription = transcriptions.get(f"{file.split('.')[0]}", None)
        if not transcription:
            print("No transcription for line_id: " + line_id)
            continue

        # (ignored if no transcription was found)
        # copy the png file to the output folder
        os.system(f"cp {path_to_png} {output_folder}")
        # create a txt file with the transcription in the output folder
        with open(os.path.join(output_folder, f"{extract_id}-{writer_id}-{line_id}.gt.txt"), "w") as f:
            f.write(transcription)

print("Done")
