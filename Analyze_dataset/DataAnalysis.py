import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

def analyze_dataset(dataset_dir, annot_dir):
    """
    Analyzes the given dataset and returns various statistics.
    """
    # Get the list of annotation files
    annot_files = os.listdir(annot_dir)

    # Initialize the class count dictionary
    class_count = {}

    # Initialize the bounding boxes per class dictionary
    bbox_per_class = {}

    # Initialize the bounding boxes per image list
    bbox_per_image = []

    # Iterate through each annotation file
    for annot_file in annot_files:
        # Parse the XML file
        tree = ET.parse(os.path.join(annot_dir, annot_file))
        root = tree.getroot()

        # Get the image size
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)

        # Get the list of objects
        objects = root.findall('object')

        # Add the number of bounding boxes to the bbox_per_image list
        bbox_per_image.append(len(objects))

        # Iterate through each object
        for obj in objects:
            # Get the class name
            class_name = obj.find('name').text

            # Update the class count dictionary
            if class_name not in class_count:
                class_count[class_name] = 0
            class_count[class_name] += 1

            # Update the bounding boxes per class dictionary
            if class_name not in bbox_per_class:
                bbox_per_class[class_name] = []
            bbox_per_class[class_name].append((float(obj.find('xmax').text) - float(obj.find('xmin').text)) * (float(obj.find('ymax').text) - float(obj.find('ymin').text)))

    # Calculate the distribution of bounding box size for each class
    bbox_size_dist = {}
    for class_name in bbox_per_class:
        bbox_sizes = bbox_per_class[class_name]
        bbox_size_dist[class_name] = {
            'min_size': min(bbox_sizes),
            'max_size': max(bbox_sizes),
            'avg_size': np.mean(bbox_sizes)
        }

    # Plot the class count and bounding boxes per image
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.bar(class_count.keys(), class_count.values())
    ax1.set_xticklabels(class_count.keys(), rotation=90)
    ax1.set_title('Class count')
    ax2.hist(bbox_per_image)
    ax2.set_title('Bounding boxes per image')
    plt.show()

    # Plot the bounding boxes per class
    fig, ax = plt.subplots()
    ax.bar(bbox_per_class.keys(), [len(bbox_per_class[class_name]) for class_name in bbox_per_class])
    ax.set_xticklabels(bbox_per_class.keys(), rotation=90)
    ax.set_title('Bounding boxes per class')
    plt.show()

    # Print the distribution of bounding box size for each class
    print('Distribution of bounding box size for each class:')
    for class_name in bbox_size_dist:
        print(class_name)
        print(f"Min size: {bbox_size_dist[class_name]['min_size']}")
        print(f"Max size: {bbox_size_dist[class_name]['max_size']}")
        print(f"Avg size: {bbox_size_dist[class_name]['avg_size']}")


dataset_dir = '/path/to/your/dataset'
annot_dir = '/path/to/your/annotation/files'

analyze_dataset(dataset_dir, annot_dir)

# Note:-  Make sure to replace /path/to/your/dataset
# and /path/to/your/annotation/files with the actual paths to your dataset and annotation files.