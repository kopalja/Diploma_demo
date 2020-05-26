#############################################################
# Generate video by drawing bounding boxes into the video.
# Only for debbuding purposses.
#############################################################
import time
import argparse
from edgetpu.detection.engine import DetectionEngine
from PIL import Image
from PIL import ImageDraw
import cv2
import numpy
import sys
from tracker.Tracker_Wrapper import Tracker_Wrapper

def resize_image(img):
    height, width, _ = img.shape
    border = (width - height) // 2
    img = img[0 : height, border : border + height]
    return cv2.resize(img, (args.size, args.size))

def draw_boxes(detections, draw):
    for obj in detections:
        box = [b * args.size for b  in obj.bounding_box.flatten().tolist()]
        draw.rectangle(box, outline='red') if obj.label_id else draw.rectangle(box, outline='blue')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type = str, default = "models/mobilenet_v1_0_300/model/output_tflite_graph_edgetpu.tflite", help = "Path to model (.tflite)")
    parser.add_argument('--input', type = str, default = "videos/vid1.MOV", help='Input video')
    parser.add_argument('--output', type = str, default = 'project.avi', help = 'Path to generated video')
    parser.add_argument('--size', default = 300, help='Input frame resolution.')
    args = parser.parse_args()

    # 1) Init
    iou_tracker = Tracker_Wrapper(0, 0.75, 0.1, 30, python = False)    
    engine = DetectionEngine(args.model)
    vidcap = cv2.VideoCapture(args.input)
    output_frames = []
    start = time.time()

    num_of_frames = 0
    while True:
        num_of_frames += 1
        success, img = vidcap.read()
        if not success:
            break
        
        # Process frame
        image_cv2 = resize_image(img)
        image_pil = Image.fromarray(image_cv2)
        draw = ImageDraw.Draw(image_pil)

        # Run inference and update track
        detections = engine.detect_with_input_tensor(image_cv2.flatten(), threshold=0.3, top_k=10)
        iou_tracker.update_tracks(detections)

        # Draw detection and save output frame
        draw_boxes(detections, draw)
        output_frames.append(numpy.array(image_pil))


    # Print results
    print('Number of processed frames: {0}'.format(num_of_frames))
    print('Time {0}'.format(time.time() - start))
    print('Cars detected {0}'.format(iou_tracker.get_tracked_number()))

    # Generate video
    out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*'DIVX'), 30, (args.size, args.size))
    for i in range(len(output_frames)):
        out.write(output_frames[i])
    out.release()


