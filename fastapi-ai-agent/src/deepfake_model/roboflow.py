import subprocess
import os
import torch
from inference_sdk import InferenceHTTPClient
import requests
from PIL import Image
from io import BytesIO
from torch.utils.model_zoo import load_url
from scipy.special import expit
from pathlib import Path

def check_path_exists(path):

    if not os.path.exists(path):
        print(f"Error: The path {path} does not exist.")
        return False
    return True
def download_image(image_url, save_dir='./data'):
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Fetch the image from the URL
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an error for failed requests
    
    # Open the image and save it
    folder_length = len(os.listdir(save_dir))
    image = Image.open(BytesIO(response.content))
    image_path = os.path.join(save_dir, f"downloaded_image_{folder_length}.jpg")
    image.save(image_path)
    
    return image_path


class Evaluator:
    def __init__(self):
        pass
    
    def roboflow_model(self, image_url):
        CLIENT = InferenceHTTPClient(
            api_url="https://classify.roboflow.com",
            api_key="B7VSO3J34QqMsMmeBwWz"
        )
        result = CLIENT.infer(image_url, model_id="deepfake-detection-using-yolo/1")
        return result['confidence']

    def dire_model(self, image_url):
        original_dir = os.getcwd()
        os.chdir('model/DIRE')
        command = ["python", "demo.py", "-f", image_url, "-m", "/weights/lsun_adm.pth"]
        subprocess.check_call(command)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        last_six_chars = output.strip()[-6:]
        os.chdir(original_dir)
        return float(last_six_chars)

    def dfdc_model(self, url, type, model_choice = 'EfficientNetAutoAttB4', dataset_choice = 'DFDC'):
        '''
        :param url: The path to the image or video
        :param type: The type of the input, either 'image' or 'video'
        :param model_choice: The model to use, either 'EfficientNetB4', 'EfficientNetB4ST', 'EfficientNetAutoAttB4', 'EfficientNetAutoAttB4ST', 'Xception'
        :param dataset_choice: The dataset to use, either 'DFDC' or 'FFPP'

        :return: The probability of the image or video being a deepfake
        '''
        original_dir = os.getcwd()
        os.chdir("./model/icpr2020dfdc/notebook")
        import sys
        sys.path.append('..')

        from blazeface import FaceExtractor, BlazeFace, VideoReader
        from architectures import fornet,weights
        from isplutils import utils
        """
        Choose an architecture between
        - EfficientNetB4
        - EfficientNetB4ST
        - EfficientNetAutoAttB4
        - EfficientNetAutoAttB4ST
        - Xception
        """
        model_set = set(['EfficientNetB4', 'EfficientNetB4ST', 'EfficientNetAutoAttB4', 'EfficientNetAutoAttB4ST', 'Xception'])
        if model_choice not in model_set:
            net_model = 'EfficientNetAutoAttB4'
        else:
            net_model = model_choice
        """
        Choose a training dataset between
        - DFDC
        - FFPP
        """
        if dataset_choice not in ['DFDC', 'FFPP']:
            train_db = 'DFDC'
        else:
            train_db = dataset_choice
        device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        face_policy = 'scale'
        face_size = 224
        model_url = weights.weight_url['{:s}_{:s}'.format(net_model,train_db)]
        net = getattr(fornet,net_model)().eval().to(device)
        net.load_state_dict(load_url(model_url,map_location=device,check_hash=True))
        transf = utils.get_transformer(face_policy, face_size, net.get_normalizer(), train=False)
        facedet = BlazeFace().to(device)
        facedet.load_weights("../blazeface/blazeface.pth")
        facedet.load_anchors("../blazeface/anchors.npy")
        if type == "video":
            videoreader = VideoReader(verbose=False)
            frames_per_video = 32
            video_read_fn = lambda x: videoreader.read_frames(x, num_frames=frames_per_video)
            face_extractor = FaceExtractor(video_read_fn=video_read_fn,facedet=facedet)
            vid_faces = face_extractor.process_video(url)
            faces_t = torch.stack( [ transf(image=frame['faces'][0])['image'] for frame in vid_faces if len(frame['faces'])] )
            with torch.no_grad():
                faces_pred = net(faces_t.to(device)).cpu().numpy().flatten()
            os.chdir(original_dir)
            return expit(faces_pred.mean())
        elif type == "image":
            face_extractor = FaceExtractor(facedet=facedet)
            img_url = os.path.abspath(os.path.join(os.getcwd(), "../../..", url))
            img = Image.open(img_url)
            im_real_faces = face_extractor.process_image(img=img)
            img_face = im_real_faces['faces'][0]
            faces_t = torch.stack( [ transf(image=im)['image'] for im in [img_face] ] )

            with torch.no_grad():
                faces_pred = torch.sigmoid(net(faces_t.to(device))).cpu().numpy().flatten()
            os.chdir(original_dir)
            return faces_pred[0]
        
    def evaluate(self, url):
        '''
        :param url: The path to the image or video
        :return: The probability of image being a deepfake
        '''
        url = os.path.normpath(url)
        if not check_path_exists(url):
            print("Error: The path does not exist.")
            return 0.0
        file_name, file_extension = os.path.splitext(url)
        if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
            results = []
            results.append(self.roboflow_model(url))
            if torch.cuda.is_available():
                results.append(self.dire_model(url))
            #results.append(self.dfdc_model(url, type="image"))
            result = sum(results) / len(results)
            return result
        elif file_extension.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
            result = self.dfdc_model(url, type="video")
            return result

def misinfo_detector_roboflow(image_url):
    '''
    Take in an image path and return the deepfake detection results.
    '''
    image_path = download_image(image_url, "./data")
    eval = Evaluator()
    result = eval.evaluate(image_path)
    return result

if __name__ == "__main__":
    print("Testing the deepfake detection model...")
    image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNzIq4l1yMTP49R7vm8kWgY09FAhW9skpcFA&s"
    result = misinfo_detector_roboflow(image_url)
    print(result)