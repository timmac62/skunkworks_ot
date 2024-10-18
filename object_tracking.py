import jetson_inference
import jetson_utils
import argparse
import math
import socket

# Define the host and port (must match the server's details)
host = '127.0.0.1'
port = 12345

# Define a simple tracker class
class ObjectTracker:
    def __init__(self):
        self.objects = {}  # Dictionary to store object IDs and their last known positions
        self.next_id = 0   # The next unique identifier for new objects

        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update(self, detections):
        updated_objects = {}

        # Iterate over all detections
        for detection in detections:
            class_id = net.GetClassDesc(detection.ClassID)
            if "person" in class_id.lower():
                center_x = (detection.Left + detection.Right) / 2
                center_y = (detection.Top + detection.Bottom) / 2

                # Find the object ID of the closest tracked object
                object_id, min_distance = None, float('inf')
                for oid, (ox, oy) in self.objects.items():
                    distance = math.sqrt((center_x - ox) ** 2 + (center_y - oy) ** 2)
                    if distance < min_distance and distance < 50:  # Distance threshold
                        object_id, min_distance = oid, distance

                # If a matching object is found, update its position
                if object_id is not None:
                    updated_objects[object_id] = (center_x, center_y)
                else:
                    # Otherwise, assign a new ID to the new object
                    updated_objects[self.next_id] = (center_x, center_y)
                    object_id = self.next_id
                    self.next_id += 1

                # Print the detection with its unique identifier
#                print(f"Detected OMG {net.GetClassDesc(detection.ClassID)} ID {object_id} with confidence {detection.Confidence:.2f} at top-left ({detection.Left:.0f}, {detection.Top:.0f})")
                messagetosend = f"ID: {object_id}, x: {center_x}, y: {center_y}"
                self.client_socket.sendto(messagetosend.encode(), (host, port))

        # Update the tracked objects with the current frame's detections
        self.objects = updated_objects

# Parse the command-line arguments
parser = argparse.ArgumentParser(description="Run object detection with simple tracking using NVIDIA Jetson Inference")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to use, e.g., ssd-mobilenet-v2, ssd-inception-v2")
parser.add_argument("--camera", type=str, default="/dev/video0", help="camera device to use (e.g., /dev/video0 for USB webcam)")
parser.add_argument("--width", type=int, default=640, help="width of camera stream")
parser.add_argument("--height", type=int, default=480, help="height of camera stream")
parser.add_argument("-hc", "--hide_camera", action="store_true", default=False, help="do not display camera stream")
args = parser.parse_args()

hide_camera = args.hide_camera

# Load the object detection network
net = jetson_inference.detectNet(args.network, threshold=0.5)

# Create the camera and display
camera = jetson_utils.videoSource(args.camera, argv=['--input-width=' + str(args.width), '--input-height=' + str(args.height)])
display = jetson_utils.videoOutput("display://0")  # Use "display://0" to show output on screen

# Create an object tracker
tracker = ObjectTracker()

# Process frames until user exits
while display.IsStreaming():
    # Capture the image
    img = camera.Capture()

    # Perform object detection
    detections = net.Detect(img)

    # Update tracker with the current frame's detections
    tracker.update(detections)

    if not hide_camera:
        # Render the image
        display.Render(img)

        # Update the display
        display.SetStatus(f"Object Detection & Tracking | Network {args.network} | {net.GetNetworkFPS():.0f} FPS")

# Release resources
camera.Close()
display.Close()