#import tf_keras as keras  # Импортируем tf-keras - это совместимая версия Keras для работы с .h5 моделями
#from tf_keras.models import load_model  # Загружаем функцию load_model из tf_keras, чтобы открыть модель
from keras.models import load_model
from PIL import Image, ImageOps  # Installing pillow instead of PIL
import numpy as np
#import keras
#import tensorflow
#print (keras.__version__,tensorflow.__version__)
#2.10.0 !, 2.15.0
#pip uninstall tensorflow keras
def classification(model, class_names, image):

  # Disable scientific notation for clarity
  np.set_printoptions(suppress=True)

  # Load the model
  model = load_model(model, compile=False)

  # Load the labels
  class_names = open(class_names, "r", encoding="UTF-8").readlines()

  # Create the array of the right shape to feed into the keras model
  # The 'length' or number of images you can put into the array is
  # determined by the first position in the shape tuple, in this case 1
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  # Replace this with the path to your image
  image = Image.open(image).convert("RGB")

  # resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
  image_array = np.asarray(image)

  # Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  # Load the image into the array
  data[0] = normalized_image_array

  # Predicts the model
  prediction = model.predict(data)
  index = np.argmax(prediction)
  class_name = class_names[index]
  confidence_score = prediction[0][index]
  return(class_name[2:], confidence_score)
  # Print prediction and confidence score
  #print("Class:", class_name[2:], end="")
  #print("Confidence Score:", confidence_score)