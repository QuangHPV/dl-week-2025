import subprocess
import os
import torch
from inference_sdk import InferenceHTTPClient

def check_path_exists(path):
    if not os.path.exists(path):
        print(f"Error: The path {path} does not exist.")
        return False
    return True

def roboflow_model(image_url):
    from inference_sdk import InferenceHTTPClient
    CLIENT = InferenceHTTPClient(
        api_url="https://classify.roboflow.com",
        api_key="B7VSO3J34QqMsMmeBwWz"
    )
    result = CLIENT.infer(image_url, model_id="deepfake-detection-using-yolo/1")
    return result['confidence']


def dire_model(image_url):
    original_dir = os.getcwd()
    os.chdir('model/DIRE')
    command = ["python", "demo.py", "-f", image_url, "-m", "/weights/lsun_adm.pth"]
    subprocess.check_call(command)
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
    last_six_chars = output.strip()[-6:]
    os.chdir(original_dir)
    return float(last_six_chars)

def dfdc_model(url, type, model_choice = 'EfficientNetAutoAttB4', dataset_choice = 'DFDC'):
    original_dir = os.getcwd()
    os.chdir("model/icpr2020dfdc/notebook")
    import torch
    from torch.utils.model_zoo import load_url
    import matplotlib.pyplot as plt
    from scipy.special import expit
    from PIL import Image

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
        img = Image.open(url)
        im_real_faces = face_extractor.process_image(img=img)
        img_face = im_real_faces['faces'][0]
        faces_t = torch.stack( [ transf(image=im)['image'] for im in [img_face] ] )

        with torch.no_grad():
            faces_pred = torch.sigmoid(net(faces_t.to(device))).cpu().numpy().flatten()
        os.chdir(original_dir)
        return faces_pred[0]

def main(url):
    if not check_path_exists(url):
        print("Error: The path does not exist.")
        return
    file_name, file_extension = os.path.splitext(url)
    if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
        result1 = roboflow_model(url)
        if torch.cuda.is_available():
            result2 = dire_model(url)
        else:
            result2 = 0
        result3 = dfdc_model(url, type="image")
        if (result1 > 0.5) or (result2 > 0.5) or (result3 > 0.5):
            print("Deepfake detected.")
        elif (0.3 < result1 < 0.5) or (0.3 < result2 < 0.5) or (0.3 < result3 < 0.5):
            print("Likely Deepfake Detected.")
        else:
            print("No Deepfake Detected.")
    elif file_extension.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        result = dfdc_model(url, type="video")
        if result > 0.5:
            print("Deepfake detected.")
        elif 0.3 < result < 0.5:
            print("Likely Deepfake Detected.")
        else:
            print("No Deepfake Detected.")
if __name__ == "__main__":
    main("/Users/phonghoang/Downloads/id0_id16_0001.mp4")