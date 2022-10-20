import torchvision
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import torch
import numpy as np
from PIL import Image
from torchvision.models.detection import FasterRCNN_MobileNet_V3_Large_FPN_Weights
from torchvision import ops
import random


class FastRCNNDetector:
    def __init__(self,
                 iou_treshold=0.1,
                 prob_treshold=0.75,
                 transform=None
                 ):
        '''
        iou_threshold - iou metric threshold for non-max suppression
        prob_threshold - min probability to detect object
        transform - transformation applied to image
        '''

        self.model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(
            weights=FasterRCNN_MobileNet_V3_Large_FPN_Weights.COCO_V1
        )
        self.model.eval()
        self.pretrained_images_size = 224
        self.iou_treshold = iou_treshold
        self.prob_treshold = prob_treshold

        self.transform = transform
        if self.transform is None:
            self.transform = A.Compose(
                [
                    ToTensorV2()
                ]
            )

    def get_prediction(self, img_path: str, save_path: str = None) -> np.array:
        '''
        img_path - path of input image
        Return image with drawing on it bboxes with labels.
        '''
        img = np.array(
            Image.open(img_path)
        )
        preprocessed_img = self.__image_preprocessing(img)

        pred = self.model(torch.stack([preprocessed_img]))

        scores = pred[0]['scores']

        # drop bboxes with low propabilty
        bboxes = pred[0]['boxes'][scores > self.prob_treshold]
        scores = scores[scores > self.prob_treshold]

        # suppress bboxes with intersections
        non_max_suppression_items = ops.nms(bboxes, scores, self.iou_treshold)

        bboxes = bboxes.detach().numpy()[non_max_suppression_items]

        if bboxes.shape == (4,):
            bboxes = bboxes.reshape(1, 4)

        result_img = self.__plot_bboxes(
            img,
            self.__scale_bboxes(img, bboxes).astype(np.uint16),
        )

        if save_path:
            Image.fromarray(result_img).save(save_path)

        return result_img

    def __image_preprocessing(self, img: np.array) -> np.array:
        '''
        img - input image
        Apply preprocessing pipeline to image.
        It's interpolation to pretrained_images_size, than scalint to interval [0, 1]
        and than apply self.transform.
        '''
        preprocessed_img = cv2.resize(
            img,
            (self.pretrained_images_size, self.pretrained_images_size),
            interpolation=cv2.INTER_CUBIC
        )
        preprocessed_img = preprocessed_img.astype(np.float) / 255
        preprocessed_img = self.transform(image=preprocessed_img)['image'].float()

        return preprocessed_img

    def __plot_bboxes(self,
                      img: np.array,
                      bboxes: np.array,
                      ) -> np.array:
        '''

        '''
        labels = random.sample(range(1, 100), bboxes.shape[0])

        for bbox, label in zip(bboxes, labels):
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(img, str(label), (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return img

    def __scale_bboxes(self, img: np.array, bboxes: np.array) -> np.array:
        '''
        img - image with original shape
        bboxes - bboxes on image with shape pretrained_images_size
        Find bboxes coordinates on original img with.
        '''
        x_scale, y_scale = (
            self.pretrained_images_size / img.shape[0],
            self.pretrained_images_size / img.shape[1]
        )
        bboxes[:, [0, 2]] /= y_scale
        bboxes[:, [1, 3]] /= x_scale

        return bboxes


predictor = FastRCNNDetector(
    iou_treshold=0.1,
    prob_treshold=0.25
)
