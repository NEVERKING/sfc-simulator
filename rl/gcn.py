from __future__ import absolute_import, division, print_function
import tensorflow as tf

import tensorflow.keras as keras
import tensorflow.keras.layers as layers


class GraphCNN(layers.Layer):
    def __init__(self, inputs, input_dim, hid_dims, output_dim,
                 max_depth, act_fn, adj_mats, masks):
        """
        :param inputs: 结点输入
        :param input_dim: 结点输入维度
        :param hid_dims: 隐藏层维度 [d1,d2]
        :param output_dim: 输出层维度 [y]
        :param max_depth: 图的最大深度
        :param act_fn: 激活函数
        """
        super(GraphCNN, self).__init__(name='gcn')

        self.input_layer = tf.keras.Input(shape=input_dim, name='input')

        self.inputs = inputs
        self.input_dim = input_dim
        self.hid_dims = hid_dims
        self.output_dim = output_dim
        self.max_depth = max_depth
        self.act_fn = act_fn
        self.adj_mats = adj_mats
        self.masks = masks

        # initialize message passing transformation parameters
        # h: x -> x' 升高维度
        self.prep_weights, self.prep_bias = \
            self.init_hid_layers(self.input_dim, self.hid_dims, self.output_dim)

        # f: x' -> e
        self.proc_weights, self.proc_bias = \
            self.init_hid_layers(self.output_dim, self.hid_dims, self.output_dim)

        # g: e -> e
        self.agg_weights, self.agg_bias = \
            self.init_hid_layers(self.output_dim, self.hid_dims, self.output_dim)

        # graph message passing
        self.outputs = self.forward()

    def init_hid_layers(self, input_dim, hid_dims, output_dim):
        weights = []
        biases = []

        # hidden layers
        curr_in_dim = input_dim
        for hid_dim in hid_dims:
            weights.append(self.add_weight(shape=(curr_in_dim, hid_dim),
                                           initializer=keras.initializers.RandomNormal(),
                                           trainable=True))
            biases.append(self.add_weight(shape=(hid_dim,),
                                          initializer=keras.initializers.Zeros(),
                                          trainable=True))
            curr_in_dim = hid_dim

        # output layer
        weights.append(self.add_weight(shape=(curr_in_dim, output_dim),
                                       initializer=keras.initializers.RandomNormal(),
                                       trainable=True))
        biases.append(self.add_weight(shape=(output_dim,),
                                      initializer=keras.initializers.Zeros(),
                                      trainable=True))
        return weights, biases

    @tf.function
    def call(self):
        x = self.input_layer

        # 1. raise x into higher dimension 将输入 x 升高维度 x'
        for l in range(len(self.prep_weights)):
            x = tf.matmul(x, self.prep_weights[l]) + self.prep_bias[l]
            x = self.act_fn(x)

        # 2.
        for d in range(self.max_depth):
            # work flow: index_select -> f -> masked assemble via adj_mat -> g
            y = x

            # process the features on the nodes
            for l in range(len(self.proc_weights)):
                y = tf.matmul(y, self.proc_weights[l]) + self.proc_bias[l]
                y = self.act_fn(y)

            # message passing
            y = tf.sparse.sparse_dense_matmul(self.adj_mats[d], y)

            # aggregate child features
            for l in range(len(self.agg_weights)):
                y = tf.matmul(y, self.agg_weights[l]) + self.agg_bias[l]
                y = self.act_fn(y)

            # remove the artifact from the bias term in g
            y = y * self.masks[d]

            # assemble neighboring information
            x = x + y
        return x


if __name__ == '__main__':
    print("test")
    #
    # GraphCNN(inputs=, input_dim=, hid_dims=, output_dim=,
    #          max_depth=, act_fn=tf.nn.leaky_relu, adj_mats=, masks=)
