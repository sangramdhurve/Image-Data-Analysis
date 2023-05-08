import os
import json
import argparse

def coco_to_yolo(coco_dir, images_dir, annotations_file, output_dir):
    """
    Converts a COCO dataset to YOLO format.
    """
    # Read the annotations file
    with open(annotations_file, 'r') as f:
        data = json.load(f)

    # Initialize the class dictionary
    classes = {}
    for i, category in enumerate(data['categories']):
        classes[category['id']] = i

    # Iterate through each image
    for image in data['images']:
        # Get the image path
        image_path = os.path.join(images_dir, image['file_name'])

        # Get the image size
        image_width = image['width']
        image_height = image['height']

        # Initialize the YOLO annotation file
        yolo_file = os.path.join(output_dir, os.path.splitext(image['file_name'])[0] + '.txt')

        # Iterate through each annotation for the current image
        for annotation in data['annotations']:
            if annotation['image_id'] == image['id']:
                # Get the class index
                class_index = classes[annotation['category_id']]

                # Get the bounding box coordinates
                x, y, w, h = annotation['bbox']
                x_center = x + w / 2
                y_center = y + h / 2
                x_center /= image_width
                y_center /= image_height
                w /= image_width
                h /= image_height

                # Write the annotation to the YOLO file
                with open(yolo_file, 'a') as f:
                    f.write(f"{class_index} {x_center} {y_center} {w} {h}\n")


# coco_dir: Path to the directory containing the COCO dataset.
coco_dir = '/path/to/coco'
# images_dir: Path to the directory containing the images of the COCO dataset.
images_dir = '/path/to/coco/images'
# annotations_file: Path to the COCO annotations file.
annotations_file = '/path/to/coco/annotations.json'
# output_dir: Path to the directory where the YOLO annotations files will be saved.

output_dir = '/path/to/yolo'
# call the function
coco_to_yolo(coco_dir, images_dir, annotations_file, output_dir)
