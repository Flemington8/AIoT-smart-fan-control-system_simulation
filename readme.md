This is a python project which using ChatGPT API to deterimine to open the fan base on temperature.

environment configuration:
Python 3.11
conda install requests
pip install paho-mqtt

parameter configuration：
客户端数量number of clients = 10 (so that each client has 300 data)
全局轮global epoch = 10
本地轮local epoch = 5
device = RTX 4060 mobile

net:
batchsize = 64
Linear1 13 * 16
Linear2 16 * 1
activation function = sigmoid
optimizer = SGD
loss function = MSEloss reduction = 'mean'
learning rate = 0.01
