import tensorflow as tf
import pandas as pd
import numpy as np

def putONE(data,arr):
    if data == 0:
        arr[0] = 1.0
    elif data == 2:
        arr[1] = 1.0
    elif data == 4:
        arr[2] = 1.0
    elif data == 6:
        arr[3] = 1.0
    elif data == 8:
        arr[4] = 1.0   

data_set = pd.read_csv('final_data.csv')
data_set = data_set.astype('float32')

data_set2 = pd.read_csv('DataSet 2018-11-19 10-12-28.csv')
data_set2 = data_set.astype('float32')

# we put the features into X (and not x) and the observation to Y (and not y)
#graph=tf.Graph()

x = tf.placeholder(tf.float32, [None,64])
y_ = tf.placeholder(tf.float32, [None,5])
W = tf.Variable(tf.zeros([64,5]))
b = tf.Variable(tf.zeros([5]))
y = tf.nn.softmax(tf.matmul(x, W) + b)

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.001).minimize(cross_entropy)
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

print(y,y_)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
for j in range(10):
    for i in range(len(data_set)):
        X = data_set.iloc[i, :-2].values
        X = X.reshape(1,64)
        Y = data_set.iloc[i, 65:].values
        Y_new = np.zeros(5,dtype=float)
        putONE(Y[0],Y_new)
        #print(Y_new)
        Y_new = Y_new.reshape(1,5)
        if i == 0:
            _xs = X
            _ys = Y_new
        _xs = np.vstack([_xs,X])
        _ys = np.vstack([_ys,Y_new])
    sess.run(train_step, feed_dict={x:_xs, y_: _ys})
    print(j, sess.run(accuracy, feed_dict={x:_xs, y_: _ys}))
 
for i in range(len(data_set2)):
    asd = data_set2.iloc[i, :-2].values
    asd = asd.reshape(1,64)
    if i%100 == 0:
        print('prediction: ', y.eval(session=sess, feed_dict = {x: asd}))

