from itertools import product
from collections import defaultdict

import numpy as np
from skimage.feature import greycomatrix, greycoprops
from skimage.measure import regionprops

DEFAULT_PROPERTIES = ('contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM')

def get_glcm_feature_names(distances, angles, properties):
    # column names for GLCM feats
    props_names = list(map(lambda x: '_'.join(x), product(properties, map(str, distances), map(str, map(np.rad2deg, angles)))))
    return props_names


def _get_uint_dtype_for_masked_img(n_bins):
    
    # NOTE: this will already error for int values > 2^64
    # also gives weird results as we approach 2^64
    necessary_bits = np.log2(n_bins)
    if necessary_bits < 8:
        return np.uint8
    elif necessary_bits < 16:
        return np.uint16
    elif necessary_bits < 32:
        return np.uint32
    elif necessary_bits < 64:
        return np.uint64
    else:
        raise ValueError(f'No uint dtype available to represent {n_bins} intensity bins')
        

def get_glcm_features_masked(img, mask, distances, angles=(0,), properties=DEFAULT_PROPERTIES, n_bins=255):

    # clip and make int
    # TODO: error on too high n_bins?
    dtype = _get_uint_dtype_for_masked_img(n_bins)
    img = (np.clip(img, 0, 1) * (n_bins - 1)).astype(dtype)
    
    # make input for masked GLCM:
    # 1) set bg to zero
    # 2) set everything else +1 
    img_for_masked_glcm = img.copy()
    img_for_masked_glcm[~ mask] = 0
    img_for_masked_glcm[mask] += 1 

    # get glcm, but ignore first row & column (co-ocurrence with 0 := background)
    glcm = greycomatrix(img_for_masked_glcm, distances, angles, n_bins+1)
    glcm = glcm[1:,1:]
    
    return np.stack([greycoprops(glcm, prop=p) for p in properties])


def get_glcm_features_per_label(img, labels, distances, angles=(0,), properties=DEFAULT_PROPERTIES, n_bins=255):
    '''
    get GLCM features for each object in an image
    
    Parameters
    ==========
    
    img: float array
        normalized intensity image, only values in (0,1) are considered
    labels: int array
        labels of objects in img
    n_bins: int
        number of intensity bins to use for GLCM calculation
    
    Returns
    =======
    property_dict: dict
        dictionary mapping property name (str) to list of property values for each object
        additional key 'label' maps to list of corresponding object labels
    
    '''
    property_dict = defaultdict(list)
    property_names = get_glcm_feature_names(distances, angles, properties)
    
    for rprop in regionprops(labels, img):
        features = get_glcm_features_masked(rprop.intensity_image, rprop.image, distances, angles, properties, n_bins)
        property_dict['label'].append(rprop.label)
        for name, feat in zip(property_names, features.flat):
            property_dict[name].append(feat)
    
    return property_dict