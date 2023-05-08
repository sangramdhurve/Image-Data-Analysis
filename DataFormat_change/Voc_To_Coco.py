import os
import json
import xml.etree.ElementTree as ET
import argparse

def voc_to_coco(voc_dir, output_file):
    """
    Converts a Pascal VOC dataset to COCO format.
    """
    # Initialize the COCO annotations dictionary
    coco = {'images': [], 'annotations': [], 'categories': []}
    annotation_id = 1

    # Create the category dictionary
    category_dict = {}
    with open(os.path.join(voc_dir, 'classes.txt'), 'r') as f:
        classes = f.read().splitlines()
    for i, cls in enumerate(classes):
        category_dict[cls] = {'id': i + 1, 'name': cls, 'supercategory': 'object'}
        coco['categories'].append(category_dict[cls])

    # Get the image and annotation paths
    image_dir = os.path.join(voc_dir, 'JPEGImages')
    annotation_dir = os.path.join(voc_dir, 'Annotations')

    # Iterate through each image
    for filename in os.listdir(image_dir):
        image_id = int(os.path.splitext(filename)[0])

        # Add the image to the COCO dictionary
        image_dict = {'id': image_id, 'file_name': filename, 'height': 0, 'width': 0}
        coco['images'].append(image_dict)

        # Get the corresponding annotation file
        annotation_file = os.path.join(annotation_dir, str(image_id) + '.xml')

        # Parse the annotation file
        root = ET.parse(annotation_file).getroot()

        # Get the image size
        image_width = int(root.find('size/width').text)
        image_height = int(root.find('size/height').text)
        image_dict['width'] = image_width
        image_dict['height'] = image_height

        # Iterate through each object in the annotation file
        for obj in root.findall('object'):
            # Get the category name and id
            category_name = obj.find('name').text
            category_id = category_dict[category_name]['id']

            # Get the bounding box coordinates
            xmin = int(obj.find('bndbox/xmin').text)
            ymin = int(obj.find('bndbox/ymin').text)
            xmax = int(obj.find('bndbox/xmax').text)
            ymax = int(obj.find('bndbox/ymax').text)

            # Add the annotation to the COCO dictionary
            annotation_dict = {'id': annotation_id, 'image_id': image_id, 'category_id': category_id,
                               'bbox': [xmin, ymin, xmax - xmin, ymax - ymin], 'area': (xmax - xmin) * (ymax - ymin),
                               'iscrowd': 0}
            coco['annotations'].append(annotation_dict)
            annotation_id += 1

    # Write the COCO annotations file
    with open(output_file, 'w') as f:
        json.dump(coco, f)


# voc_dir: Path to the directory containing the Pascal VOC dataset.
voc_dir = '/path/to/voc'
# output_file: Path to the output COCO annotations file.
output_file = '/path/to/coco/annotations.json'
# call the function
voc_to_coco(voc_dir, output_file)
