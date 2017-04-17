import tensorflow as tf
from tensorflow.python import pywrap_tensorflow
import os

model_dir = 'inceptionv3_s_finetuned'
checkpoint_name = 'model.ckpt-460'

checkpoint_path = os.path.join(model_dir, checkpoint_name)

reader = tf.train.NewCheckpointReader(checkpoint_path)
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()

print('tensor names:')
print('-----------------------------------------------------------------------')
for key in var_to_shape_map:
  print('tensor names:', key)
  # print(reader.get_tensor(key)) # print value in tensor variables
