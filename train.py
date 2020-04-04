import efficientnet.keras as efn
from tensorflow.keras.utils import plot_model
from IPython.display import Image
from IPython.display import Image
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras import models
from tensorflow.keras import layers
# parameters
#batch_size = 48 no batch size, good for small dataset
width = 150
height = 150
input_shape = (height, width, 3)

# loading pretrained conv base model
efficient_model = efn.EfficientNetB0(weights = 'imagenet', include_top = False, input_shape = input_shape)

# The path to the dataset directory
train_dir = './Dataset/train/Stop sign/'
validation_dir = './Dataset/validation/Stop sign/'
test_dir = './Dataset/test/Stop sign/'

train_datagen = ImageDataGenerator( rescale= 1./255,
                                    zoom_range=[1.2,1.5],
                                    rotation_range=40,
                                    width_shift_range=0.2,
                                    height_shift_range=0.2,
                                    shear_range=0.2,
                                    horizontal_flip=True,
                                    fill_mode='nearest'
                                    )

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(height, width),
    class_mode= 'binary')

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(height, width),
    class_mode='binary')
# img = load_img(train_dir+'1d01568a9f8b528f.jpg')  # 这是一个PIL图像
# x = img_to_array(img)  # 把PIL图像转换成一个numpy数组，形状为(3, 150, 150)
# x = x.reshape((1,) + x.shape)  # 这是一个numpy数组，形状为 (1, 3, 150, 150)
#
# i = 0
# for batch in train_datagen.flow(x, batch_size=1,
#                           save_to_dir='preview', save_prefix='cat1', save_format='jpeg'):
#     i += 1
#     if i > 2:
#         break


model = models.Sequential()
model.add(efficient_model)
model.add(layers.GlobalMaxPooling2D(name="gap"))

