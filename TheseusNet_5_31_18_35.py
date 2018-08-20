# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 10:24:58 2018

@author: desktop
"""
# -*- coding: utf-8 -*-


import numpy as np
from keras.models import Sequential, Model
from keras.layers import Input, Convolution2D, merge,Conv2D, Conv2DTranspose, SeparableConv2D
from keras.layers import BatchNormalization, Dense, Dropout, Activation, PReLU, ELU
from keras.layers import MaxPooling2D, UpSampling2D,Flatten,concatenate, AveragePooling2D 
from keras import regularizers 
from keras.layers.normalization import BatchNormalization as bn
from keras import initializers
from keras import backend as K


#%%

#This is based on Model 5
#Added inception blcok after 5th
# Had to remove 2 conv blocks because its OOM.  Added kernel 9 to last layers
#3, put kernels back to 9, 4 conv blocks
#6 - added kernel3 back into model
#& Trying 2nd sep conv block
#8 got rid of 2nd sepconv block.  Added 5th conv block
#9 added a tower 3 to inceptoin block with larger kernels
#10 pulled 5th conv block, added tower with block 2 as inputs
#14 based on 10, playing with activations
#16 56, 60, 61 lines changed to PReLUs
#prelus to elus
#27 elus on the FC layers
#28 regularizers for block 1
#30 regularizers to 0.02
#31 changes rest of relus to elus
#35 increased regs

def VGG19(input_specs, settings):
    
    input_shape = (
        input_specs["INPUT_Y_SIZE"],
        input_specs["INPUT_X_SIZE"],
        input_specs["n_channels"])
    
    # define the setting for the model
#    KERNEL_SIZE = settings["KERNEL_SIZE"]
    KERNEL_SIZE1 = (3,3)
    KERNEL_SIZE2 = (5,5)
    KERNEL_SIZE3 = (7,7)
    NUM_CLASSES = settings['NUM_CLASSES']
    drop_out_rate = settings['drop_out_rate']    
    
    # define input shape
    inputs = Input(shape = input_shape)
    
    #separable Conv Layer
    conv0 = SeparableConv2D(128, KERNEL_SIZE1, padding = "same", depth_multiplier = 1)(inputs)
    conv0 = ELU(alpha=1.0)(inputs)
   
    # first conv block
    conv1 = Convolution2D(256, KERNEL_SIZE1, kernel_regularizer=regularizers.l2(0.015), padding="same")(conv0)
    conv1 = ELU(alpha=1.0)(conv0)
    conv1 = Convolution2D(256, KERNEL_SIZE1, kernel_regularizer=regularizers.l2(0.015), padding="same")(conv1)
    conv1 = ELU(alpha=1.0)(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    
   # second conv block
    conv2 = Convolution2D(256, KERNEL_SIZE1, padding="same", activation="tanh")(pool1)
    conv2 = Convolution2D(256, KERNEL_SIZE1, padding="same", activation="tanh")(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    
    # third conv block
    conv3 = Convolution2D(256, KERNEL_SIZE2, padding="same", activation="tanh")(pool2)
    conv3 = Convolution2D(256, KERNEL_SIZE2, padding="same", activation="tanh")(conv3)
    conv3 = Convolution2D(256, KERNEL_SIZE2, padding="same", activation="tanh")(conv3)
    conv3 = Convolution2D(256, KERNEL_SIZE2, padding="same", activation="tanh")(conv3)
    pool3 = AveragePooling2D(pool_size=(2, 2))(conv3)

    #Ending inception block
    tower_1 = Conv2D(128, KERNEL_SIZE1, padding='same')(pool3)
    tower_1 = ELU(alpha=1.0)(pool3)
    tower_1 = Conv2D(128, KERNEL_SIZE1, padding='same')(tower_1)
    tower_1 = ELU(alpha=1.0)(tower_1)
    tower_2 = Conv2D(128, KERNEL_SIZE3, padding='same')(pool3)
    tower_2 = ELU(alpha=1.0)(pool3)
    tower_2 = Conv2D(128, KERNEL_SIZE3, padding='same')(tower_2)
    tower_2 = ELU(alpha=1.0)(tower_2)
    output = concatenate([tower_1, tower_2], axis=1)
    
    # fully connected layer
    flat = Flatten(name = 'flatten')(output)
    fc = Dense(1024, kernel_regularizer=regularizers.l2(0.15), name = 'fc1')(flat)  
    fc = ELU(alpha=1.0)(flat)
    fc = Dropout( drop_out_rate )(fc)
    fc = Dense(1024, kernel_regularizer=regularizers.l2(0.15), name = 'fc2')(fc) 
    fc = ELU(alpha=1.0)(fc)
#    fc = Dropout( drop_out_rate )(fc)
    fc = Dense(NUM_CLASSES, activation = "linear", name = 'predictions')(fc)
    # define model and compile
    model = Model(inputs=inputs, outputs=fc)
    return model
#
#if __name__ == '__main__':
#    main()

    
    
    