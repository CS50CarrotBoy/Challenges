\# YOLOv8 FPV Target Detection and Automated Targeting Challenge



\## Challenge Overview



In this challenge, you will develop a computer vision system capable of processing a drone video feed locally using YOLOv8. The system will identify and classify military vehicles within the video stream, generate target coordinates for detected objects, and provide control inputs that could be used by an operator or automated system to automatically center and target the selected object.



The objective is to build a complete proof-of-concept pipeline that ingests video, performs object detection, calculates target positions, and demonstrates how camera movement could be automated to maintain focus on a selected object.



A suggested dataset of approximately 2,000 labelled images is accessible here https://universe.roboflow.com/mamad-vira/military-vehicle-m5bvw for model training and validation. A 9-minute test video for evaluation can be found here https://www.youtube.com/watch?v=w9hzh2Yn13c. You may use other datasets and test videos if you wish.



\*\*Estimated Time:\*\* 3 Hours



\---



\## Learning Objectives



By the end of this challenge, you should be able to:



\* Prepare and train a YOLOv8 object detection model.

\* Understand the fundamentals of object detection and classification.

\* Perform inference on recorded CCTV footage.

\* Extract object locations from detection results.

\* Calculate target coordinates within a video frame.

\* Design a basic target-selection and tracking strategy.

\* Evaluate model performance using test footage.

\* Discuss practical limitations of automated visual tracking systems.



\---



\## Scenario



You have been tasked with developing a prototype FPV targeting system.



The system must:



1\. Ingest a video feed locally.

2\. Detect and classify objects within the scene.

3\. Identify a target military vehicle.

4\. Generate coordinates representing the target's position in the frame.

5\. Determine the movement required to center the target.



The provided 2,000-image dataset should be used to train and validate the detection model. Once trained, the model should be evaluated using the supplied 9-minute test video.



\---



\## Functional Requirements



\### Video Ingestion



The solution must:



\* Read video from a local file.

\* Process video frame-by-frame.

\* Perform inference using YOLOv8.

\* Display detection results.



\### Object Detection



The solution must:



\* Detect objects present in each frame.

\* Assign classifications.

\* Display confidence scores.

\* Draw bounding boxes around detected objects.



\### Target Selection



The solution must:



\* Select a target object from the detections.

\* Justify the selection logic.



Examples:



\* Highest confidence detection.

\* Largest detected object.

\* Specific object class.

\* Closest object to the centre of the frame.



\### Coordinate Generation



The solution must calculate:



\* Bounding box centre coordinates.

\* Frame centre coordinates.

\* Horizontal offset.

\* Vertical offset.



Example:



Frame Size: 1920 x 1080



Target Bounding Box:



\* X = 800

\* Y = 300

\* Width = 200

\* Height = 400



Calculated Target Centre:



\* X = 900

\* Y = 500



Frame Centre:



\* X = 960

\* Y = 540



Offset:



\* Horizontal = -60

\* Vertical = -40



\---



\## UAS Control Design



Design a method to automate UAS movement.



The system should determine:



\* Move Left

\* Move Right

\* Move Up

\* Move Down

\* Hold Position



You do not need physical hardware.



Instead, produce a control algorithm demonstrating how commands would be generated from target position data.



Example:



| Offset Condition            | Action    |

| --------------------------- | --------- |

| X < -50                     | Yaw Left  |

| X > 50                      | Yaw Right |

| Y < -50                     | Pitch Up   |

| Y > 50                      | Pitch Down |



\---



\## Success Criteria



To complete the challenge, participants must:



1\. Train or fine-tune a YOLOv8 model.

2\. Run inference against the provided test video.

3\. Detect and classify objects successfully.

4\. Generate target coordinates.

5\. Calculate object offsets.

6\. Demonstrate tracking behaviour on the test video.

7\. Document system performance and limitations.



\---



\## Deliverables



Present:



\### 1. Trained Model



\* YOLOv8 model file.

\* Training configuration.



\### 2. Detection Demonstration



\* Screenshot(s) of detections.

\* Annotated output video or video clips.



\### 3. Target Tracking Report



Include:



\* Selected target criteria.

\* Example target coordinates.

\* Frame offset calculations.

\* Tracking logic.



\### 4. UAS Control Design



Document:



\* UAS control logic.

\* Movement thresholds.

\* Assumptions made.



\### 5. Performance Evaluation



Report:



\* Detection accuracy observations.

\* False positives.

\* False negatives.

\* Areas for improvement.



\## Prerequisites



Participants should have:



\* Python 3.10+

\* YOLOv8 installed

\* OpenCV

\* NumPy

\* Basic Python knowledge

\* Understanding of object detection concepts



\---



\## Constraints



\* The supplied test video must be used for evaluation.

\* No manual intervention during automated target tracking demonstrations.



\---



\## Ethical and Legal Notice



This challenge is intended for educational purposes to demonstrate computer vision, object detection, and automated camera control concepts.



Participants should focus on the technical implementation of object detection and tracking rather than identification of individuals. Any deployment involving real-world surveillance must comply with applicable privacy, data protection, and organizational policies.

