import cv2
from ultralytics import YOLO

def test_hand_sign_model():
    model_path = 'runs/detect/hand_sign_model/weights/best.pt'

    # Load your trained model
    model = YOLO(model_path)

    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        
        # Run inference
        results = model(frame)
        
        # Visualize results
        annotated_frame = results[0].plot()
        cv2.imshow("Hand Sign Detection", annotated_frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test_hand_sign_model()


