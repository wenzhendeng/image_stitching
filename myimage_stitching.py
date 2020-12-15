
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", type=str, default='images/scottsdale/', help="path to input directory of images to stitch")
    parser.add_argument("--output", type=str, default='test1.jpg', help="path to the output image")
    parser.add_argument("--crop", type=int, default=1, help="whether to crop out largest rectangular region")
    return parser.parse_args()


def main():
    # 加载参数
    args = parser_args()
    print(args.images)
    # 获取图像列表
    imagePaths = sorted(list(paths.list_images(args.images)))
    images = []

    # 加载图像
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        images.append(image)

    # 拼接
    print("[INFO] stitching images...")
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)

    if status == 0:
        # status=0时，表示拼接成功
        if args.crop > 0:
            # 边界填充
            stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))

            # 转为灰度图进行并二值化
            gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

            # 获取轮廓
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)

            mask = np.zeros(thresh.shape, dtype="uint8")
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

            minRect = mask.copy()
            sub = mask.copy()

            while cv2.countNonZero(sub) > 0:
                minRect = cv2.erode(minRect, None)
                sub = cv2.subtract(minRect, thresh)

            cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)

            # 取出图像区域
            stitched = stitched[y:y + h, x:x + w]

        cv2.imwrite(args.output, stitched)
    else:
        print("[INFO] image stitching failed ({})".format(status))


if __name__=='__main__':
    main()