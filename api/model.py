import tensorflow as tf

def identity_block(input_tensor, channels):
    nb_filter1, nb_filter2, nb_filter3 = channels
    
    x = tf.keras.layers.Conv2D(nb_filter1, (1, 1))(input_tensor)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)

    x = tf.keras.layers.Conv2D(nb_filter2, (3, 3), padding='same')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)

    x = tf.keras.layers.Conv2D(nb_filter3, (1, 1))(x)
    x = tf.keras.layers.BatchNormalization()(x)

    x = tf.keras.layers.Add()([x, input_tensor])
    x = tf.keras.layers.Activation('relu')(x)
    return x

def conv_block(input_tensor, kernel_size, channels, strides=(2, 2)):
    nb_filter1, nb_filter2, nb_filter3 = channels

    x = tf.keras.layers.Conv2D(nb_filter1, (1, 1), strides=strides)(input_tensor)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)

    x = tf.keras.layers.Conv2D(nb_filter2, (kernel_size, kernel_size), padding='same')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)

    x = tf.keras.layers.Conv2D(nb_filter3, (1, 1))(x)
    x = tf.keras.layers.BatchNormalization()(x)

    shortcut = tf.keras.layers.Conv2D(nb_filter3, (1, 1), strides=strides)(input_tensor)
    shortcut = tf.keras.layers.BatchNormalization()(shortcut)

    x = tf.keras.layers.Add()([x, shortcut])
    x = tf.keras.layers.Activation('relu')(x)
    return x


def doubleConv(inputs, channel):
    x = tf.keras.layers.Conv2D(filters = channel, kernel_size = 3, strides=1, padding = 'same')(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Conv2D(filters = channel, kernel_size = 3, strides=1, padding = 'same')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = identity_block(x, [channel//4, channel//2, channel])

    return x

def attention(x, g):
    theta_x = tf.keras.layers.Conv2D(filters = 1, kernel_size=1)(x)
    theta_g = tf.keras.layers.Conv2D(filters = 1, kernel_size=1)(g)
    act = tf.keras.layers.ReLU()(tf.keras.layers.add([theta_x, theta_g]))
    act = tf.keras.layers.Conv2D(filters = 1, kernel_size=1)(act)
    act = tf.keras.layers.Activation('sigmoid')(act)
    out = tf.keras.layers.multiply([x, act])
    return out

def downsample(block_input, channel, strides = (2, 2), is_first = False):
    if is_first:
        conv1 = tf.keras.layers.Conv2D(filters = channel, kernel_size = 3, strides=1, padding = 'same')(block_input)
        conv2 = tf.keras.layers.Conv2D(filters = channel, kernel_size = 3, strides=1, padding = 'same')(conv1)
        act = tf.keras.layers.ReLU()(conv2)
        return act

    x = conv_block(block_input, 3, [channel//4, channel//2, channel], strides=strides)
    return x

def upsample(block_input, block_counterpart, channel):  
    # Upsampling block
    uppool1 = tf.keras.layers.Convolution2DTranspose(channel, kernel_size=2, strides=2)(block_input)

    att = attention(uppool1, block_counterpart)
    concat = tf.keras.layers.Concatenate(axis=-1)([att, uppool1])

    x = doubleConv(uppool1, channel)
    return x

def create_model():
    input = tf.keras.layers.Input(shape=(480, 640, 3))
    norm = tf.keras.layers.Lambda(lambda x: x/255.0)(input)
    ds_block1 = downsample(norm, channel=32, is_first = True)
    ds_block2 = downsample(ds_block1, channel=64)
    ds_block3 = downsample(ds_block2, channel=128)
    ds_block4 = downsample(ds_block3, channel=256)
    ds_block5 = downsample(ds_block4, channel=512)
    ds_block6 = downsample(ds_block5, channel=1024)

    us_block5 = upsample(ds_block6, ds_block5, channel=512)
    us_block4 = upsample(us_block5, ds_block4, channel=256)
    us_block3 = upsample(us_block4, ds_block3, channel=128)
    us_block2 = upsample(us_block3, ds_block2, channel=64)
    us_block1 = upsample(us_block2, ds_block1, channel=32)

    x = tf.keras.layers.Conv2D(filters=1, kernel_size=3, strides=1, activation='sigmoid', padding = 'same')(us_block1)
    
    model = tf.keras.models.Model(inputs = input, outputs = x)
    return model