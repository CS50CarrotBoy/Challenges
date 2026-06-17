# SAIT Interview - Data Engineering

This challenge has been created to assess the suitability of candidates with regards to handling operational data. Candidates are assessed not only by the output of their program, but by considerations made along the way and their design process.

Candidates may use any language to accomplish this task, however it is strongly recommended to use a JuPyTer notebook for these tasks.

## The Brief

The SAIT has been given a document (found in /data) which logs communications (SMS, Calls) between any Mobile Phones in [Undisclosed Location].

The Data is stored in the following format:

| sending_device_id | target_device_id | timestamp            |
|------------|--------------|----------------------|
| 0001       | 0002         | 2026-06-10T08:32:00Z |
| 0002       | 0004         | 2026-06-12T15:43:00Z |
| 0004       | 0003         | 2026-06-13T11:05:00Z |

## Taskings

Your task is to parse through the data in order to perform the following tasks:
1. List how many unique numbers are present
2. List the top 5 most frequent numbers
3. Display a visualisation of PED usage by hour
4. Identify the PED(s) which communicate with the largest amount of **unique** devices

### Extension

Upon completion of the aforementioned tasks, Candidates are free to use the rest of their allotted time to add any other features.

One such example would be to produce a "Degrees of Separation" algorithm that takes two numbers as input, and returns the shortest number of links between those two numbers or an error message if the numbers are not connected.

Example Output when searching for links between Devices 0001 and 0003:
```  
Path:  
0001 -> 0002  
0002 -> 0004  
0004 -> 0003

Number of Links: 3
```