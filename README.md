# PID Ball Balancing System

This project is a PID (Proportional, Integral, Derivative) control system designed to balance a ball on a platform. The system utilizes a Raspberry Pi 3 and servo motors to adjust the platform's angle in real-time, maintaining the ball's position.

## Bill of Materials

Below is a list of components used in the PID Ball Balancing System, along with their sources and prices.

| Item | Quantity | Source | Price |
|------|----------|--------|-------|
| Servo Motors | 4 | [Amazon](#) | $18.39 |
| Servo Driver HAT | 1 | [Amazon](#) | $18.20 |
| 3D Printed Motor Arm | 4 | FEDC Design Center | N/A |
| 3D Printed Arm | 4 | FEDC Design Center | N/A |
| 3D Printed Base | 1 | FEDC Design Center | N/A |
| 3D Printed Couplers | 4 | FEDC Design Center | N/A |
| Universal Joints | 4 | [Amazon](#) | $10.99 |
| Raspberry Pi 3 | 1 | Provided | N/A |
| Washer Locking Nut Bolt | 4 | [Home Depot](#) | ~$6.00 |
| Wooden Base | 1 | [Home Depot](#) | ~$12.00 |
| Sq. Foot PVC Platform | 1 | [Amazon](#) | $17.47 |
| Adjustable Lamp Arm | 1 | [Amazon](#) | $19.47 |
| Logitech Webcam | 1 | [Amazon](#) | $59.99 |
| 9 V 1 A Power Supply | 1 | Provided | N/A |

## Setup and Configuration

The system's hardware assembly involves mounting the servo motors on the 3D-printed base, connecting the arms, and positioning the Raspberry Pi and camera. Detailed steps for assembly and the software setup can be found in our [Github repository](https://github.com/Eanazir/PID_system).

## System Operation

The PID controller software processes the camera feed to track the ball's position and adjusts the platform's angle using the servo motors to keep the ball centered.

## Images

![System Overview](/path/to/image1.png)
*System overview with labeled components.*

![Action Shot](/path/to/image2.png)
*The PID Ball Balancing System in operation.*

