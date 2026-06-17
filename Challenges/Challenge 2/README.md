\# Raspberry Pi Wi-Fi Monitoring Challenge



\## Challenge Overview



In this challenge, you will transform a Raspberry Pi into a wireless network monitoring station using Kismet. You will learn how wireless networks are discovered, how monitoring tools collect information from the airwaves, and how network administrators use these techniques for visibility, situational awareness, and incident response.



The goal is to configure Kismet, place a wireless adapter into monitor mode, and observe nearby wireless network activity from a controlled and authorized environment.



As part of the exercise, you will design and deploy a Raspberry Pi-based Wi-Fi monitoring sensor capable of detecting suspicious or unauthorized wireless activity. You should consider how the device could be discreetly deployed, powered for extended periods, and how collected monitoring data can be securely retrieved and analysed.



During the exercise, an unauthorized wireless network named \*\*"RogueCorp-Guest"\*\* will be introduced into the monitoring area. Participants must detect the network, investigate its characteristics, determine whether it is authorized, and recommend appropriate response actions.



\*\*Estimated Time:\*\* 3 Hours



\---



\## Learning Objectives



By the end of this challenge, you should be able to:



\* Install and configure Kismet on a Raspberry Pi.

\* Understand the difference between managed mode and monitor mode.

\* Capture and view wireless network information.

\* Identify wireless access points and client devices.

\* Navigate the Kismet web interface.

\* Understand basic wireless network reconnaissance concepts.

\* Detect suspicious or unauthorized wireless activity.

\* Consider practical deployment factors for monitoring sensors.

\* Discuss legal and ethical considerations surrounding wireless monitoring.



\---



\## Scenario



You have been asked to assist a network administrator who needs better visibility into the wireless environment around a small office.



Your task is to build and deploy a Raspberry Pi-based Wi-Fi monitoring sensor capable of identifying nearby wireless networks and presenting the collected information through Kismet.



The monitoring sensor should be designed with real-world deployment considerations in mind, including:



\* Physical placement and camouflage.

\* Power supply requirements.

\* Data storage and retention.

\* Methods for extracting or remotely accessing collected data.

\* Reliability and maintainability.



Security has received intelligence that an unauthorized wireless network named \*\*"RogueCorp-Guest"\*\* may appear within range of the office. Your monitoring solution must detect the network and gather sufficient information to support investigation and incident reporting.



When the network appears, determine:



\* When it first appeared.

\* The SSID name.

\* Signal strength.

\* Whether it is authorized.

\* Appropriate response actions.



\---



\## Success Criteria



To complete the challenge, participants must:



1\. Install Kismet successfully.

2\. Configure a compatible wireless adapter.

3\. Enable monitor mode.

4\. Launch Kismet and access the web interface.

5\. Detect and display nearby wireless networks.

6\. Identify the unauthorized SSID when it appears.

7\. Document deployment considerations for the monitoring sensor.

8\. Produce a brief incident report for the detected rogue network.



\### General Network Monitoring



Document at least:



\* Three detected access points.

\* Their channels.

\* Signal strengths.

\* Security types (e.g., WPA2, WPA3).



\### Rogue Network Investigation



Document:



\* Detection time.

\* SSID name.

\* Signal strength.

\* Channel used.

\* Whether the network is authorized.

\* Recommended response actions.



\### Deployment Considerations



Explain:



\* How the sensor would be physically deployed.

\* How it would be powered.

\* How monitoring data would be retrieved.

\* Any limitations or risks associated with the deployment.



\---



\## Deliverables



Submit:



\* Screenshot of the Kismet dashboard.

\* Short explanation of monitor mode.

\* Table containing observed wireless networks.

\* Detection report for the unauthorized SSID.

\* Description of the proposed deployment approach.

\* Brief discussion of one challenge encountered and how it was resolved.



\### Example Incident Report



| Field              | Value                                                           |

| ------------------ | --------------------------------------------------------------- |

| Detection Time     | HH:MM                                                           |

| SSID               | RogueCorp-Guest                                                 |

| Channel            | XX                                                              |

| Signal Strength    | XX dBm                                                          |

| Authorized         | No                                                              |

| Recommended Action | Report to administrator and follow incident response procedures |



\---



\## Prerequisites



Participants should have:



\* Raspberry Pi with Raspberry Pi OS installed.

\* Internet access for package installation.

\* Supported Wi-Fi adapter capable of monitor mode.

\* Basic Linux command-line knowledge.



\---



\## Constraints



\* Do not attempt to connect to unauthorized networks.

\* Do not perform packet injection, deauthentication, or denial-of-service attacks.

\* Only monitor networks within a legal and authorized environment.

\* Focus on observation, detection, and analysis rather than offensive actions.

\* Follow established reporting procedures when suspicious wireless activity is detected.



\---



\## Ethical and Legal Notice



Wireless monitoring should only be performed on networks and environments where you have explicit authorization.



This challenge is intended solely for educational and defensive cybersecurity learning. The purpose of the exercise is to practice wireless monitoring, identification of unauthorized wireless activity, and incident reporting.



Participants must not attempt to gain access to networks, interfere with wireless communications, or conduct offensive security testing.



