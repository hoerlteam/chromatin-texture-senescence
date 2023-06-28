//@File dir (style="directory")
//@Integer n_tiles

print(dir);
print(n_tiles);

// define dataset
run("Define dataset ...", "define_dataset=[Manual Loader (TIFF only, ImageJ Opener)] project_filename=dataset.xml multiple_timepoints=[NO (one time-point)] " +
"multiple_channels=[NO (one channel)] _____multiple_illumination_directions=[NO (one illumination direction)] multiple_angles=[NO (one angle)] multiple_tiles=[YES (one file per tile)] "+
"image_file_directory="+dir+" image_file_pattern=tile_{xxx}.tif tiles_=0-"+(n_tiles-1)+" calibration_type=[Same voxel-size for all views] "+
"calibration_definition=[Load voxel-size(s) from file(s)] imglib2_data_container=[ArrayImg (faster)]");

// load tile config
run("Load TileConfiguration from File...", "select="+dir+"/dataset.xml tileconfiguration="+dir+"/tile_config_bigstitcher.txt use_pixel_units keep_metadata_rotation");


run("Calculate pairwise shifts ...", "select="+dir+"/dataset.xml process_angle=[All angles] process_channel=[All channels] process_illumination=[All illuminations] "+
"process_tile=[All tiles] process_timepoint=[All Timepoints] method=[Phase Correlation] downsample_in_x=1 downsample_in_y=1 downsample_in_z=1");

run("Filter pairwise shifts ...", "select="+dir+"/dataset.xml filter_by_link_quality min_r=0.6 max_r=1 max_shift_in_x=0 max_shift_in_y=0 max_shift_in_z=0 max_displacement=0");


run("Optimize globally and apply shifts ...", "select="+dir+"/dataset.xml process_angle=[All angles] process_channel=[All channels] process_illumination=[All illuminations] "+
"process_tile=[All tiles] process_timepoint=[All Timepoints] relative=2.500 absolute=3.500 global_optimization_strategy=[Two-Round using Metadata to align unconnected Tiles] fix_group_0-0");

run("Fuse dataset ...", "select="+dir+"/dataset.xml process_angle=[All angles] process_channel=[All channels] process_illumination=[All illuminations] "+
"process_tile=[All tiles] process_timepoint=[All Timepoints] bounding_box=[All Views] downsampling=1 interpolation=[Linear Interpolation] "+
"pixel_type=[16-bit unsigned integer] interest_points_for_non_rigid=[-= Disable Non-Rigid =-] blend produce=[Each timepoint & channel] fused_image=[Display using ImageJ] "+
"define_input=[Manually define range of input data (in next dialog)] min=0 max=65535 display=[precomputed (fast, complete copy in memory before display)] min_intensity=0 max_intensity=255");

saveAs("Tiff", dir + "/fused.tif");

// really close!
run("Quit");
eval("script", "System.exit(0);");