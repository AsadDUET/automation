# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

import numpy as np
import tensorflow as tf
from picamera import PiCamera
camera=PiCamera()

camera.resolution=(224,224)
camera.start_preview(alpha=200)
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class s_motor(object):
	def __init__(self,a1,a2,b1,b2,delay):
		self.a1=a1
		self.a2=a2
		self.b1=b1
		self.b2=b2
		self.delay=delay
		GPIO.setup(self.a1,GPIO.OUT)
		GPIO.setup(self.a2,GPIO.OUT)
		GPIO.setup(self.b1,GPIO.OUT)
		GPIO.setup(self.b2,GPIO.OUT)
		self.set_step(0,0,0,0)
	def forward(self,steps):
		for i in range(0,steps):
			self.set_step(1,0,1,0)
			time.sleep(self.delay)
			self.set_step(0,1,1,0)
			time.sleep(self.delay)
			self.set_step(0,1,0,1)
			time.sleep(self.delay)
			self.set_step(1,0,0,1)
			time.sleep(self.delay)

	def backward(self,steps):
		for i in range(0,steps):
			self.set_step(1,0,0,1)
			time.sleep(self.delay)
			self.set_step(0,1,0,1)
			time.sleep(self.delay)
			self.set_step(0,1,1,0)
			time.sleep(self.delay)
			self.set_step(1,0,1,0)
			time.sleep(self.delay)
	def set_step(self,a1,a2,b1,b2):
		GPIO.output(self.a1,a1)
		GPIO.output(self.a2,a2)
		GPIO.output(self.b1,b1)
		GPIO.output(self.b2,b2)



#sonar_readings
TRIG = 18
ECHO = 16
distance=15
sonar_readings=[15,15,15,15,15]
print ("Distance Measurement In Progress")
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
def read_sonar():
        for i in range(5):
            GPIO.output(TRIG, False)
            print ("Waiting For Sensor To Settle" )
            time.sleep(.05)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            while GPIO.input(ECHO)==0:
                pulse_start = time.time()
            while GPIO.input(ECHO)==1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            if (distance>=3 and distance<=28):
                sonar_readings[i]=distance
            else:
                pass
        distance=sum(sonar_readings)/len(sonar_readings)
        print ("Distance:",distance,"cm")




def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)
  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def asad ():
  file_name = "photo.jpg"
  model_file = "retrained_graph.pb"
  label_file = "retrained_labels.txt"
  input_height = 224
  input_width = 224
  input_mean = 128
  input_std = 128
  input_layer = "input"
  output_layer = "final_result"

  parser = argparse.ArgumentParser()
  parser.add_argument("--image", help="image to be processed")
  parser.add_argument("--graph", help="graph/model to be executed")
  parser.add_argument("--labels", help="name of file containing labels")
  parser.add_argument("--input_height", type=int, help="input height")
  parser.add_argument("--input_width", type=int, help="input width")
  parser.add_argument("--input_mean", type=int, help="input mean")
  parser.add_argument("--input_std", type=int, help="input std")
  parser.add_argument("--input_layer", help="name of input layer")
  parser.add_argument("--output_layer", help="name of output layer")
  args = parser.parse_args()

  if args.graph:
    model_file = args.graph
  if args.image:
    file_name = args.image
  if args.labels:
    label_file = args.labels
  if args.input_height:
    input_height = args.input_height
  if args.input_width:
    input_width = args.input_width
  if args.input_mean:
    input_mean = args.input_mean
  if args.input_std:
    input_std = args.input_std
  if args.input_layer:
    input_layer = args.input_layer
  if args.output_layer:
    output_layer = args.output_layer

  graph = load_graph(model_file)
  with tf.Session(graph=graph) as sess:
      distance=15
      while True:
          if (distance>3 and distance<14):
              time.sleep(2)
              camera.capture("photo.jpg",use_video_port=True)
              print("capturing")
              t = read_tensor_from_image_file(file_name,
                                              input_height=input_height,
                                              input_width=input_width,
                                              input_mean=input_mean,
                                              input_std=input_std)

              input_name = "import/" + input_layer
              output_name = "import/" + output_layer
              input_operation = graph.get_operation_by_name(input_name);
              output_operation = graph.get_operation_by_name(output_name);



              results = sess.run(output_operation.outputs[0],
                          {input_operation.outputs[0]: t})
              results = np.squeeze(results)

              top_k = results.argsort()[-5:][::-1]
              labels = load_labels(label_file)
              print(labels[top_k[0]], results[top_k[0]])




              if (top_k[0]==0):
                  mh.backward(150)
                  ma.forward(60)
                  mb.backward(50)
                  mh.forward(150)
                  mb.forward(50)
                  ma.backward(60)

              if (top_k[0]==1):
                  mh.backward(150)
                  ma.forward(60)
                  mb.backward(100)
                  mh.forward(150)
                  mb.forward(100)
                  ma.backward(60)

              if (top_k[0]==2):
                  mh.backward(150)
                  ma.forward(60)
                  mb.backward(75)
                  mh.forward(150)
                  mb.forward(75)
                  ma.backward(60)
              for i in range(5):
                  GPIO.output(TRIG, False)
                  print ("Waiting For Sensor To Settle" )
                  time.sleep(.05)
                  GPIO.output(TRIG, True)
                  time.sleep(0.00001)
                  GPIO.output(TRIG, False)
                  while GPIO.input(ECHO)==0:
                      pulse_start = time.time()
                  while GPIO.input(ECHO)==1:
                      pulse_end = time.time()
                  pulse_duration = pulse_end - pulse_start
                  distance = pulse_duration * 17150
                  distance = round(distance, 2)
                  if (distance>=3 and distance<=28):
                      sonar_readings[i]=distance
                  else:
                      pass
              distance=sum(sonar_readings)/len(sonar_readings)
              print ("Distance:",distance,"cm")
          else:
              for i in range(5):
                  GPIO.output(TRIG, False)
                  print ("Waiting For Sensor To Settle" )
                  time.sleep(.05)
                  GPIO.output(TRIG, True)
                  time.sleep(0.00001)
                  GPIO.output(TRIG, False)
                  while GPIO.input(ECHO)==0:
                      pulse_start = time.time()
                  while GPIO.input(ECHO)==1:
                      pulse_end = time.time()
                  pulse_duration = pulse_end - pulse_start
                  distance = pulse_duration * 17150
                  distance = round(distance, 2)
                  if (distance>=3 and distance<=28):
                      sonar_readings[i]=distance
                  else:
                      pass
              distance=sum(sonar_readings)/len(sonar_readings)
              print ("Distance:",distance,"cm")


mb=s_motor(6,13,19,26,.05)
mh=s_motor(27,22,10,9,.01)
ma=s_motor(2,3,4,17,.03)
asad()
