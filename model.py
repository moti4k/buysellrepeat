import transformers
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model(r'billion_model')
im_size = (224, 224)
VIT_model = transformers.TFViTModel.from_pretrained('google/vit-base-patch32-224-in21k')
types = {0: 'arnault',
         1: 'bezos',
         2: 'billy',
         3: 'bill_gates',
         4: 'brin',
         5: 'buffit',
         6: 'buterin',
         7: 'chan',
         8: 'cruise',
         9: 'durov',
         10: 'dwayne_jonson',
         11: 'ellish',
         12: 'ellon_musk',
         13: 'franconise',
         14: 'friedkin',
         15: 'gosling',
         16: 'jay_z',
         17: 'koch',
         18: 'larry_page',
         19: 'quandt',
         20: 'reevs',
         21: 'rihanna',
         22: 'sandleer',
         23: 'schwarzengger',
         24: 'scott',
         25: 'spielberg',
         26: 'stallone',
         27: 'travis',
         28: 'west',
         29: 'zuckerberg', }

def model_pred(path: str, transposer: tuple = (0, 3, 2, 1), divider: int = 255, subtrahend=0.5, factor=2,
               dtype=tf.float32):
    image = tf.io.read_file(path)
    image = tf.io.decode_image(image, expand_animations=False, channels=3)
    image = tf.image.resize(image, im_size)
    image = tf.reshape(image, (1, *im_size, 3))
    image = tf.transpose(image, transposer)
    image = tf.cast(image, dtype)
    image = image / divider
    image = image - subtrahend
    image = image * factor
    to_model = VIT_model.predict(image, verbose=0).pooler_output
    result = model.predict(to_model)
    to_return = types[np.argmax(result[:, :30])]
    return (to_return, fr'css/images/billion/{to_return}.jpg')

