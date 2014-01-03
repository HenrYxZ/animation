animation
=========

## Face Motion tracking using Stereo Vision.

1. Use a specific color in every point you want to track in the face. The program is set to find red points, you can change it by modifying color_test.py.
2. Record the video of the face moving with a stereo camera or with two normal cameras, in the second case make sure to have the cameras in a fixed position and to measure the relative positions of the cameras including rotation.
3. Write your extrinsic matrices in project4.py in "RT_1" and "RT_2". Look at http://docs.opencv.org/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html for more information about intrinsic and extrinsic matrices.
4. Calibrate both cameras to get the principal point and the focal lenght of each one; you can calibrate cameras using this Matlab toolbox http://www.vision.caltech.edu/bouguetj/calib_doc/
5. Run 
`` python project4.py ``
to process the two videos. The 3D positions of every points will be store in "log.txt". Also some testing images will be store in the imgs folder, so you can look if the points detection were effective or not.
6. You can look a 3D animation of the points by running 
`` python gui.py ``

## Dependencies

This project uses python, OpenCV and OpenGL, GLU and GLUT
You may install them to run it.




