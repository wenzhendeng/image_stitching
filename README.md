# image_stitching
1、对多张图片进行基于SIFT的特征检测算法，如果符合最小拼接要求大的关键点`matchKeypoints`数量，使用`OpenCV-Python`自带的`stitching`方法进行全景拼接，但是对于拼接后的黑边裁剪效果不好，可以修改优化。
2、运行：python image_stitching.py --images images/scottsdale --output output.png --crop 1
   注意：如果匹配失败的话检查opencv-contrib-python的版本，我的是4.1.2.30，用3.3.0.10则可能匹配失败。
