# Chromatin texture analysis of (induced) senescence in IMR90 cells

## Workflow for STED data

* 1. ```feature_extraction_sted.ipynb``` to extract GLCM texture and auxiliary features from .h5 files created during automated acquisitions
* 2. ```quality_control_sted.ipynb``` for ML-assisted quality control (good/bad image classification) based on features
* 3. ```oldyoung_cls_sted.ipynb``` and ```feature_embedding_plots.ipynb``` for old/young classification of treated cells and generation of t-SNE plots / example image extraction.

## Workflow for confocal data

* 1. For overview images from automated STED runs: ```overview_extraction_from_h5.ipynb``` to save individual images as TIFF
* 2. Stitch into large images using ```bigstitcher_overview_stitch_wrapper.ipynb```
* 3. Segment individual cells using ```cellpose_segmentation.ipynb```
* 4. ```feature_extraction_overview.ipynb``` to extract GLCM texture and auxiliary features for each cell from overview images and segmentation masks
* 5. ```oldyoung_cls_overview.ipynb``` and ```feature_embedding_plots.ipynb``` for old/young classification of treated cells and generation of t-SNE plots / example image extraction.