import os
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(voc_annotation_path, yolo_annotation_path, class_names):
    """
    Convert Pascal VOC annotation format to YOLO annotation format.

    Parameters:
    - voc_annotation_path: str, path to the directory containing VOC annotation files (.xml).
    - yolo_annotation_path: str, path to the directory where YOLO annotation files (.txt) will be saved.
    - class_names: list of str, names of classes.

    Returns:
    None
    """
    # Check if the output directory exists, create it if it doesn't exist
    if not os.path.exists(yolo_annotation_path):
        os.makedirs(yolo_annotation_path)

    # Define class mapping
    class_map = {}
    for i, name in enumerate(class_names):
        class_map[name] = i

    # Loop over annotation files
    for filename in os.listdir(voc_annotation_path):
        if not filename.endswith('.xml'):
            continue

        # Parse XML file
        xml_path = os.path.join(voc_annotation_path, filename)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Get image size
        size = root.find('size')
        width = float(size.find('width').text)
        height = float(size.find('height').text)

        # Loop over object instances
        with open(os.path.join(yolo_annotation_path, filename[:-4] + '.txt'), 'w') as f:
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                bbox = obj.find('bndbox')
                xmin = float(bbox.find('xmin').text)
                ymin = float(bbox.find('ymin').text)
                xmax = float(bbox.find('xmax').text)
                ymax = float(bbox.find('ymax').text)

                # Convert bounding box to YOLO format
                x_center = (xmin + xmax) / (2 * width)
                y_center = (ymin + ymax) / (2 * height)
                w = (xmax - xmin) / width
                h = (ymax - ymin) / height

                # Write to YOLO annotation file
                class_id = class_map[class_name]
                f.write('{} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(class_id, x_center, y_center, w, h))

    print('Pascal VOC annotation files have been successfully converted to YOLO annotation format.')



# the path to the directory containing the Pascal VOC annotation files (voc_annotation_path)
voc_annotation_path = './data/voc_annotations'
# the path to the directory where YOLO annotation files will be saved (yolo_annotation_path)
yolo_annotation_path = './data/yolo_annotations'
# the list of class names (class_names).
class_names = ['car', 'person', 'dog']
# call the function
convert_voc_to_yolo(voc_annotation_path, yolo_annotation_path, class_names)
