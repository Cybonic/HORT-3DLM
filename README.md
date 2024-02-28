# HORTO-3DLM Dataset
The HORTO-3DLM Dataset contains 3D LiDAR and GNSS/localization data for the purpose of 3D LiDAR-based place recognition, localization and mapping in horticultural environments.

## [Data Download](https://nas-greenbotics.isr.uc.pt/drive/d/s/x4eZ5aPL96blS0i7xNKIl0iJOtkdU7QR/h3YJb7wuqCZpV9NNxgeITnGTRsDJeVNY-a7eAQXUnGQs#file_id=799704328662196403) | 

## Content
1. [Updates](#1-updates)
2. [Dataset](#2-dataset)
3. [Citation](#3-citation)

## 1. Updates 
- **25/02/2024** HORTO-3DLM v2.0 added GTJ34 and ON22 sequences
- **1/12/2024** HORTO-3DLM v1.0 Uploaded


## 2. Dataset

***Table Caption: Summary of all sequences***

The ***Seq.*** column contains the sequence names. The ***M***, ***Y***, and ***C*** columns refer to the month, year, and country of recording, respectively. The total distance (***Dist***) of each sequence is measured in meters, while the scan size refers to the number of points in each scan.


| Seq.  | M    | Y    | C  | Nº Scans | Nº Rows | Dist. [m] | Scan Size | Plantation Type       |
|-------|------|------|----|----------|---------|-----------|-----------|-----------------------|
| ON22  | Nov. | 2022 | UK | 7974     | 4       | 514       | 48k       | Apple (open)          |
| OJ22  | July | 2022 | UK | 4361     | 3       | 206       | 50k       | Apple (open)          |
| OJ23  | June | 2023 | UK | 7229     | 3       | 459       | 46k       | Cherry (open)         |
| SJ23  | June | 2023 | UK | 6389     | 3       | 742       | 48k       | Strawberry (polytunnels) |
| ON23  | Nov. | 2023 | FR | 3086     | 5       | 966       | 105k      | Apple (open)          |
| GTJ23 | June | 2023 | PT | 661      | 3       | 202       | 60k       | Tomato (greenhouse)   |


### Trajectories and recording setups

<p align="center">
  <img src="figs/sequences.jpg" width="400" />
  <img src="figs/robots.jpg" width="350" /> 
</p>


***Sequence ON23*** was recorded in November 2023, in an orchard in Metz, France,  with an 16-beam Ouster 3D LiDAR and an SBG GNSS/INS system (without RTK) mounted on a Clearpath Husky mobile platform. To address the low LiDAR resolution, the original scans were merged to increase point density, resulting in sub-maps with approximately 100k points per sub-map. This operation reduced the original sequence from 25836 scans to 3086 sub-maps in total.

***Sequence GTJ23*** was recorded in June of 2023, in a tomato plantation within a greenhouse, in Coimbra, Portugal,  with a 64-beam Ouster 3D LiDAR mounted on a Clearpath Jackal mobile platform. Due to signal interference caused by the greenhouse structure, the GNSS signal was unreliable. Therefore, the ground-truth positions were computed using a SLAM approach.

![Figure](figs/3dmap.jpg) 

### V1.0:
These sequences were recorded in England, UK, using a Clearpath Husky mobile robot equipped with a Velodyne VLP32 3D LiDAR (10Hz) and a ZED-F9P RTK-GPS (5Hz).

- OJ23: recorded in November 2022,
- OJ22: recorded in November 2022,
- SJ23: strawberries within polytunnels with a table-top growing system.
- ON22: recorded in November 2022, in an orchard in Metz, France.


![Figure](figs/horto-3dlm.png)

 

## Citation:
```
@article{barros2023orchnet,
    title={ORCHNet: A Robust Global Feature Aggregation approach for 3D LiDAR-based Place recognition in Orchards},
    author={Barros, T and Garrote, L and Conde, P and Coombes, MJ and Liu, C and Premebida, C and Nunes, UJ},
    journal={arXiv preprint arXiv:2303.00477},
    year={2023}
}
```


### TO-DO
- Add information
- Add Sensor TFs
- Add Dataset structure