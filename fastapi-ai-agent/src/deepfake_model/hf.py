from transformers import pipeline
from typing import List, Dict
import argparse
from PIL import Image
from ultralytics import YOLO
import cv2
import os
import numpy as np
import argparse
import requests
from io import BytesIO


class DeepfakeDetectionWrapper:
    def __init__(self, model_names: List[str]):
        """
        Initialize multiple models for deepfake detection.
        :param model_names: List of Hugging Face model names to use.
        """
        self.models = {name: pipeline("image-classification", model=name) for name in model_names}
    
    def predict_single_image(self, image: Image.Image) -> Dict[str, float]:
        """
        Run all models on the input image and return aggregated predictions.
        :param image: PIL Image to classify.
        :return: Dictionary of model predictions (averaged scores for each class).
        """
        results = {}
        for model_name, model in self.models.items():
            preds = model(image)
            for pred in preds:
                label = pred["label"]
                score = pred["score"]
                if label not in results:
                    results[label] = []
                results[label].append(score)
        
        # Average scores for each label
        aggregated_results = {label: sum(scores) / len(scores) for label, scores in results.items()}
        return aggregated_results

    def predict_batch_images(self, images: List[Image.Image]):
        """
        Run all models on a batch of images and return aggregated predictions.
        :param images: List of PIL images to classify.
        :return: List of dictionaries of model predictions (averaged scores for each class).
        """
        return [self.predict_single_image(image) for image in images]
    

class YOLOBoundingBoxImageWrapper:
    def __init__(self):
        """
        Initialize the YOLO model for object detection.
        """
        self.model = YOLO("yolo11n.pt")

    def process_image(self, image_path):
        """
        Process the input image and return the cropped bounding boxes.
        :param image_path: Path to the image to segment.
        :return: List of PIL images of bounding boxes and their predictions.
        """
        image = cv2.imread(image_path)
        

        # Run inference
        results = self.model(image)

        bbox_images = []  # Store extracted bounding boxes
        predictions = []  # Store predicted class names and bounding boxes

        # Process detection results
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()  # Get bounding boxes
            class_ids = result.boxes.cls.cpu().numpy().astype(int)  # Get class IDs
            names = self.model.names  # Get class name mapping

            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)  # Convert bbox coordinates to int
                class_id = class_ids[i]  # Get class ID
                class_name = names[class_id]  # Get class name

                # Extract the bounding box region
                cropped_bbox = image[y1:y2, x1:x2]

                # Convert NumPy image to PIL format
                bbox_pil = Image.fromarray(cropped_bbox)
                bbox_images.append(bbox_pil)  # Store the image

                # Store prediction details
                predictions.append({"class": class_name, "bbox": (x1, y1, x2, y2)})

        return bbox_images, predictions  # Return lists of images and predictions
    
def download_image(image_url, save_dir):
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Fetch the image from the URL
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an error for failed requests
    
    # Open the image and save it
    image = Image.open(BytesIO(response.content))
    image_path = os.path.join(save_dir, "downloaded_image.jpg")
    image.save(image_path)
    
    return image_path

def misinfo_detector_hf(image_url):
    '''
    Take in an image path and return the deepfake detection results.
    '''
    models = [
        #"prithivMLmods/AI-vs-Deepfake-vs-Real", 
        #"prithivMLmods/Deep-Fake-Detector-v2-Model", 
        "prithivMLmods/Deepfake-Detection-Exp-02-22"
    ]  


    image_path = download_image(image_url, save_dir='./')
    # Initialize YOLO segmentation model
    segmenter = YOLOBoundingBoxImageWrapper()

    
    # Extract bounding boxes as PIL images
    bbox_images, predictions = segmenter.process_image(image_path)
    human_bbox_images = []
    print(len(bbox_images), "objects detected in the image.")
    for bbox, class_name in zip(bbox_images, predictions):
        if class_name["class"] == "person":
            human_bbox_images.append(bbox)
    # Initialize YOLO segmentation model
    segmenter = YOLOBoundingBoxImageWrapper()
    
    # Extract bounding boxes as PIL images
    bbox_images, predictions = segmenter.process_image(image_path)
    human_bbox_images = []
    print(len(bbox_images), "objects detected in the image.")
    for bbox, class_name in zip(bbox_images, predictions):
        if class_name["class"] == "person":
            human_bbox_images.append(bbox)
    # for i, bbox in enumerate(bbox_images):
    #     bbox.save(f"bbox_{i}.png")
    
    ans = None
    if not bbox_images:
        ans = ["No objects detected in the image."]
    else:
        # Initialize deepfake detector
        detector = DeepfakeDetectionWrapper(models)

        # Run deepfake detection on extracted bounding boxes
        predictions = detector.predict_batch_images(human_bbox_images)

        ans = predictions
    return ans
    



# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run deepfake detection on an image.")
#     parser.add_argument("--image_path", type=str, required=True, help="Path to the input image.")
#     args = parser.parse_args()
    
#     models = [
#         "prithivMLmods/AI-vs-Deepfake-vs-Real", 
#         "prithivMLmods/Deep-Fake-Detector-v2-Model", 
#         "prithivMLmods/Deepfake-Detection-Exp-02-22"
#     ]  # Example models, replace with deepfake-specific ones
    
#     # Initialize YOLO segmentation model
#     segmenter = YOLOBoundingBoxImageWrapper()
    
#     # Extract bounding boxes as PIL images
#     bbox_images, predictions = segmenter.process_image(args.image_path)
#     human_bbox_images = []
#     print(len(bbox_images), "objects detected in the image.")
#     for bbox, class_name in zip(bbox_images, predictions):
#         if class_name["class"] == "person":
#             human_bbox_images.append(bbox)
#     # for i, bbox in enumerate(bbox_images):
#     #     bbox.save(f"bbox_{i}.png")

#     if not bbox_images:
#         print("No objects detected in the image.")
#     else:
#         # Initialize deepfake detector
#         detector = DeepfakeDetectionWrapper(models)

#         # Run deepfake detection on extracted bounding boxes
#         predictions = detector.predict_batch_images(human_bbox_images)

#         print("\nDeepfake Detection Results:")
#         for i, pred in enumerate(predictions):
#             print(f"Object {i + 1}: {pred}")