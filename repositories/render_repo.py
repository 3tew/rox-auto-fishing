import sys
import psutil
import cv2
import numpy as np
from PIL import Image

import config


def tracking_info(curTime):
    # Initialize FPS variables
    sec = curTime - config.PREV_TIME
    config.PREV_TIME = curTime
    fps = 1 / sec
    count_str = "%d time" % config.COUNT
    fps_str = "FPS: %0.1f" % fps
    # Right side
    cv2.rectangle(config.FRAME, (config.BOUNDING_BOX['width'] - (
        65 if not config.HOLD else 40), config.BOUNDING_BOX['width'] - 15), (config.BOUNDING_BOX['width'] - (
            30 if not config.HOLD else 40) + 70, config.BOUNDING_BOX['height']), (0, 255, 0) if not config.HOLD else (0, 0, 255), -1)
    cv2.putText(config.FRAME, str("Fishing..." if not config.HOLD else "Stop"), (config.BOUNDING_BOX['width'] - (
        60 if not config.HOLD else 35), config.FRAME.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0) if not config.HOLD else (255, 255, 255), 1)
    # Left side
    cv2.putText(config.FRAME, str("Limit: " + str("No" if config.LIMIT == -1 else config.LIMIT)), (0,
                config.FRAME.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(config.FRAME, str("Count: " + count_str), (0,
                config.FRAME.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(config.FRAME, str(
        fps_str), (0, config.FRAME.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)


def center_point():
    cv2.circle(config.FRAME, (0 + int(config.BOUNDING_BOX['width'] / 2), 0 + int(
        config.BOUNDING_BOX['height'] / 2)), config.RADIUS, (255, 255, 255), thickness=1, lineType=8, shift=0)
    cv2.rectangle(config.FRAME, (0 + int(config.BOUNDING_BOX['width'] / 2), 0 + int(config.BOUNDING_BOX['height'] / 2)),
                  (0 + int(config.BOUNDING_BOX['width'] / 2),
                   0 + int(config.BOUNDING_BOX['height'] / 2)),
                  (255, 255, 255), 5)


def crop_screenshot(sct):
    config.BOUNDING_BOX = {
        'left': int((75.52 * int(config.SCREEN_WIDTH)) / 100),
        'top': int((60.2 * int(config.SCREEN_HEIGHT)) / 100),
        'width': 240,
        'height': 250
    }
    config.CENTER_X = 1570
    config.CENTER_Y = 775
    sct.get_pixels(config.BOUNDING_BOX)
    config.FRAME = Image.frombytes(
        'RGB', (sct.width, sct.height), sct.image)


def show(detector):
    # แสดงรายละเอียดบนจอ
    tracking_info(config.CURRENT_TIME)
    # Center point
    center_point()
    # Rendering
    cv2.imshow('RO:X - Auto Fishing v%s' % config.VERSION,
               np.hstack([config.FRAME])) # add 'green' for mask debug
