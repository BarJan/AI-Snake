import tensorflow as tf
import pandas as pd
import numpy as np

def putONE(data,arr):

    if data == 2:
        arr[0] = 1
    elif data == 4:
        arr[1] = 1
    elif data == 6:
        arr[2] = 1
    elif data == 8:
        arr[3] = 1
    
data_set = pd.read_csv('final_data.csv')
data_set = data_set.astype('float32')

data_set2 = pd.read_csv('DataSet 2018-11-19 10-12-28.csv')
data_set2 = data_set.astype('float32')

# we put the features into X (and not x) and the observation to Y (and not y)
#graph=tf.Graph()

(hidden1_size, hidden2_size, hidden3_size, hidden4_size, hidden5_size) = (120, 80, 50, 32, 15)

x = tf.placeholder(tf.float32, [None,64])
y_ = tf.placeholder(tf.float32, [None,4])

W1 = tf.Variable(tf.truncated_normal([64, hidden1_size], stddev=0.1))
b1 = tf.Variable(tf.constant(0.9, shape=[hidden1_size]))
z1 = tf.nn.relu(tf.matmul(x,W1)+b1)

W2 = tf.Variable(tf.truncated_normal([hidden1_size, hidden2_size], stddev=0.1))
b2 = tf.Variable(tf.constant(0.9, shape=[hidden2_size]))
z2 = tf.nn.relu(tf.matmul(z1,W2)+b2)

W3 = tf.Variable(tf.truncated_normal([hidden2_size, hidden3_size], stddev=0.1))
b3 = tf.Variable(tf.constant(0.9, shape=[hidden3_size]))
z3 = tf.nn.relu(tf.matmul(z2,W3)+b3)

W4 = tf.Variable(tf.truncated_normal([hidden3_size, hidden4_size], stddev=0.1))
b4 = tf.Variable(tf.constant(0.9, shape=[hidden4_size]))
z4 = tf.nn.relu(tf.matmul(z3,W4)+b4)

W5 = tf.Variable(tf.truncated_normal([hidden4_size, hidden5_size], stddev=0.1))
b5 = tf.Variable(tf.constant(0.9, shape=[hidden5_size]))
z5 = tf.nn.relu(tf.matmul(z4,W5)+b5)

W = tf.Variable(tf.truncated_normal([hidden5_size, 4], stddev=0.1))
b = tf.Variable(tf.constant(0.9, shape=[4]))
y = tf.nn.softmax(tf.matmul(z5, W) + b)


cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy)
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

for j in range(10000):
    for i in range(len(data_set)):
        X = data_set.iloc[i, :-2].values
        X = X.reshape(1,64)
        Y = data_set.iloc[i, 65:].values
        Y_new = np.zeros(4,dtype=float)
        putONE(Y[0],Y_new)
        #print(Y_new)
        Y_new = Y_new.reshape(1,4)
        if i == 0:
            _xs = X
            _ys = Y_new
        _xs = np.vstack([_xs,X])
        _ys = np.vstack([_ys,Y_new])
    sess.run(train_step, feed_dict={x:_xs, y_: _ys})
    if j % 10 == 0:
        print(j, sess.run(accuracy,feed_dict={x: _xs, y_:_ys}))

for i in range(len(data_set2)):
    asd = data_set2.iloc[i, :-2].values
    asd = asd.reshape(1,64)
    Y1 = data_set.iloc[i, 65:].values
    Y_new1 = np.zeros(4,dtype=float)
    putONE(Y1[0],Y_new1)
    Y_new1 = Y_new1.reshape(1,4)
    if i == 0:
        _xs1 = asd
        _ys1 = Y_new1
    _xs1 = np.vstack([_xs1,asd])
    _ys1 = np.vstack([_ys1,Y_new1])
print(sess.run(accuracy,feed_dict={x: _xs1, y_:_ys1}))
