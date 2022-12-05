# coding=utf-8

# import tensorflow as tf
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


class PolicyGradient_chatbot(nn.Module):
    def __init__(self, dim_wordvec, n_words, dim_hidden, batch_size, n_encode_lstm_step, n_decode_lstm_step,
                 bias_init_vector=None, lr=0.0001):
        super(PolicyGradient_chatbot, self).__init__()
        self.dim_wordvec = dim_wordvec
        self.dim_hidden = dim_hidden
        self.batch_size = batch_size
        self.n_words = n_words
        self.n_encode_lstm_step = n_encode_lstm_step
        self.n_decode_lstm_step = n_decode_lstm_step
        self.lr = lr

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.Wemb = nn.Embedding(self.n_words, self.dim_hidden)
        self.lstm1 = nn.LSTMCell(self.dim_hidden, self.dim_hidden)
        self.lstm2 = nn.LSTMCell(self.dim_hidden, self.dim_hidden)
        self.encode_vector_W = nn.Linear(self.dim_wordvec, self.dim_hidden)
        self.encode_vector_b = nn.Linear(self.dim_hidden, self.dim_hidden)
        self.embed_word_W = nn.Linear(self.dim_hidden, self.n_words)
        if bias_init_vector is not None:
            self.embed_word_b = nn.Linear(self.n_words, self.n_words)
        else:
            self.embed_word_b = nn.Linear(self.n_words, self.n_words)

    def build_model(self):
        word_vectors = torch.zeros([self.batch_size, self.n_encode_lstm_step, self.dim_wordvec], dtype=torch.float32)
        caption = torch.zeros([self.batch_size, self.n_decode_lstm_step], dtype=torch.int64)
        caption_mask = torch.zeros([self.batch_size, self.n_decode_lstm_step], dtype=torch.float32)

        word_vectors_flat = word_vectors.view(-1, self.dim_wordvec)
        wordvec_emb = F.linear(word_vectors_flat, self.encode_vector_W, self.encode_vector_b)
        wordvec_emb = wordvec_emb.view(self.batch_size, self.n_encode_lstm_step, self.dim_hidden)

        reward = torch.zeros([self.batch_size, self.n_decode_lstm_step], dtype=torch.float32)
        state1 = (torch.zeros([self.batch_size, self.dim_hidden], dtype=torch.float32),
                  torch.zeros([self.batch_size, self.dim_hidden], dtype=torch.float32))
        state2 = (torch.zeros([self.batch_size, self.dim_hidden], dtype=torch.float32),
                  torch.zeros([self.batch_size, self.dim_hidden], dtype=torch.float32))
        loss = 0.0
        probs = []
        for i in range(self.n_decode_lstm_step):
            if i == 0:
                current_embed = torch.zeros([self.batch_size, self.dim_hidden], dtype=torch.float32)
            else:
                current_embed = self.Wemb(caption[:, i - 1])
            state1 = self.lstm1(current_embed, state1)
            state2 = self.lstm2(state1[0], state2)
            logit_words = F.linear(state2[0], self.embed_word_W, self.embed_word_b)
            max_prob_word = torch.argmax(logit_words, 1)
            probs.append(logit_words)
            if i > 0:
                loss += F.cross_entropy(logit_words, caption[:, i], ignore_index=0)
            if i < self.n_decode_lstm_step - 1:
                reward[:, i] = self.get_reward(state2[0], wordvec_emb, caption[:, i], i)
        return loss, probs, reward

        # reward = tf.placeholder(tf.float32, [self.batch_size, self.n_decode_lstm_step])
        #
        # state1 = tf.zeros([self.batch_size, self.lstm1.state_size])
        # state2 = tf.zeros([self.batch_size, self.lstm2.state_size])
        # padding = tf.zeros([self.batch_size, self.dim_hidden])
        #
        # entropies = []
        # loss = 0.
        # pg_loss = 0.  # policy gradient loss
        #
        # ##############################  Encoding Stage ##################################
        # for i in range(0, self.n_encode_lstm_step):
        #     if i > 0:
        #         tf.get_variable_scope().reuse_variables()
        #
        #     with tf.variable_scope("LSTM1"):
        #         output1, state1 = self.lstm1(wordvec_emb[:, i, :], state1)
        #         # states.append(state1)
        #
        #     with tf.variable_scope("LSTM2"):
        #         output2, state2 = self.lstm2(tf.concat([padding, output1], 1), state2)
        #
        # ############################# Decoding Stage ######################################
        # for i in range(0, self.n_decode_lstm_step):
        #     with tf.device("/cpu:0"):
        #         current_embed = tf.nn.embedding_lookup(self.Wemb, caption[:, i])
        #
        #     tf.get_variable_scope().reuse_variables()
        #
        #     with tf.variable_scope("LSTM1"):
        #         output1, state1 = self.lstm1(padding, state1)
        #
        #     with tf.variable_scope("LSTM2"):
        #         output2, state2 = self.lstm2(tf.concat([current_embed, output1], 1), state2)
        #
        #     labels = tf.expand_dims(caption[:, i + 1], 1)
        #     indices = tf.expand_dims(tf.range(0, self.batch_size, 1), 1)
        #     concated = tf.concat([indices, labels], 1)
        #     onehot_labels = tf.sparse_to_dense(concated, tf.stack([self.batch_size, self.n_words]), 1.0, 0.0)
        #
        #     logit_words = tf.nn.xw_plus_b(output2, self.embed_word_W, self.embed_word_b)
        #
        #     cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logit_words, labels=onehot_labels)
        #     cross_entropy = cross_entropy * caption_mask[:, i]
        #     entropies.append(cross_entropy)
        #     pg_cross_entropy = cross_entropy * reward[:, i]
        #
        #     pg_current_loss = tf.reduce_sum(pg_cross_entropy) / self.batch_size
        #     pg_loss = pg_loss + pg_current_loss
        #
        # with tf.variable_scope(tf.get_variable_scope(), reuse=False):
        #     train_op = tf.train.AdamOptimizer(self.lr).minimize(pg_loss)
        #
        # input_tensors = {
        #     'word_vectors': word_vectors,
        #     'caption': caption,
        #     'caption_mask': caption_mask,
        #     'reward': reward
        # }
        #
        # feats = {
        #     'entropies': entropies
        # }
        #
        # return train_op, pg_loss, input_tensors, feats

    def get_reward(self, state, wordvec_emb, caption, i):
        # state: [batch_size, dim_hidden]
        # wordvec_emb: [batch_size, n_encode_lstm_step, dim_hidden]
        # caption: [batch_size, n_decode_lstm_step]
        # i: int
        # return: [batch_size]
        state = state.unsqueeze(1).expand(-1, self.n_encode_lstm_step, -1)
        state = state.contiguous().view(-1, self.dim_hidden)
        wordvec_emb = wordvec_emb.view(-1, self.dim_hidden)
        logit_words = F.linear(state, self.embed_word_W, self.embed_word_b)
        max_prob_word = torch.argmax(logit_words, 1)
        reward = torch.zeros([self.batch_size], dtype=torch.float32)
        for j in range(self.batch_size):
            if max_prob_word[j] == caption[j, i]:
                reward[j] = 1
        return reward

        # state = tf.expand_dims(state, 1)
        # state = tf.tile(state, [1, self.n_encode_lstm_step, 1])
        # state = tf.reshape(state, [-1, self.dim_hidden])
        # wordvec_emb = tf.reshape(wordvec_emb, [-1, self.dim_hidden])
        # logit_words = tf.nn.xw_plus_b(state, self.embed_word_W, self.embed_word_b)
        # max_prob_word = tf.argmax(logit_words, 1)
        # reward = tf.zeros([self.batch_size])
        # for j in range(self.batch_size):
        #     if max_prob_word[j] == caption[j, i]:
        #         reward[j] = 1
        # return reward

    def build_generator(self):
        # word_vectors: [batch_size, n_encode_lstm_step, dim_hidden]
        # caption: [batch_size, n_decode_lstm_step + 2]
        word_vectors = torch.zeros([self.batch_size, self.n_encode_lstm_step, self.dim_hidden], dtype=torch.float32)
        caption = torch.zeros([self.batch_size, self.n_decode_lstm_step + 2], dtype=torch.long)

        state1 = torch.zeros([self.batch_size, self.lstm1.state_size])
        state2 = torch.zeros([self.batch_size, self.lstm2.state_size])
        padding = torch.zeros([self.batch_size, self.dim_hidden])

        ##############################  Encoding Stage ##################################
        for i in range(0, self.n_encode_lstm_step):
            with torch.no_grad():
                output1, state1 = self.lstm1(word_vectors[:, i, :], state1)
                output2, state2 = self.lstm2(torch.cat([padding, output1], 1), state2)

        ############################# Decoding Stage ######################################
        for i in range(0, self.n_decode_lstm_step):
            with torch.no_grad():
                if i == 0:
                    current_embed = torch.zeros([self.batch_size, self.dim_hidden])
                else:
                    current_embed = self.Wemb(caption[:, i])

                output1, state1 = self.lstm1(padding, state1)
                output2, state2 = self.lstm2(torch.cat([current_embed, output1], 1), state2)

                logit_words = F.linear(output2, self.embed_word_W, self.embed_word_b)
                max_prob_word = torch.argmax(logit_words, 1)
                caption[:, i + 1] = max_prob_word

        return caption

        # word_vectors = tf.zeros([self.batch_size, self.n_encode_lstm_step, self.dim_hidden])
        # caption = tf.zeros([self.batch_size, self.n_decode_lstm_step + 2])
        #
        # state1 = tf.zeros([self.batch_size, self.lstm1.state_size])
        # state2 = tf.zeros([self.batch_size, self.lstm2.state_size])
        # padding = tf.zeros([self.batch_size, self.dim_hidden])
        #
        # ##############################  Encoding Stage ##################################
        # for i in range(0, self.n_encode_lstm_step):
        #

    # def build_generator(self):
    #     word_vectors = tf.placeholder(tf.float32, [self.batch_size, self.n_encode_lstm_step, self.dim_wordvec])
    #
    #     word_vectors_flat = tf.reshape(word_vectors, [-1, self.dim_wordvec])
    #     wordvec_emb = tf.nn.xw_plus_b(word_vectors_flat, self.encode_vector_W, self.encode_vector_b)
    #     wordvec_emb = tf.reshape(wordvec_emb, [self.batch_size, self.n_encode_lstm_step, self.dim_hidden])
    #
    #     state1 = tf.zeros([self.batch_size, self.lstm1.state_size])
    #     state2 = tf.zeros([self.batch_size, self.lstm2.state_size])
    #     padding = tf.zeros([self.batch_size, self.dim_hidden])
    #
    #     generated_words = []
    #
    #     probs = []
    #     embeds = []
    #     states = []
    #
    #     for i in range(0, self.n_encode_lstm_step):
    #         if i > 0:
    #             tf.get_variable_scope().reuse_variables()
    #
    #         with tf.variable_scope("LSTM1"):
    #             output1, state1 = self.lstm1(wordvec_emb[:, i, :], state1)
    #             states.append(state1)
    #
    #         with tf.variable_scope("LSTM2"):
    #             output2, state2 = self.lstm2(tf.concat([padding, output1], 1), state2)
    #
    #     for i in range(0, self.n_decode_lstm_step):
    #         tf.get_variable_scope().reuse_variables()
    #
    #         if i == 0:
    #             # <bos>
    #             with tf.device('/cpu:0'):
    #                 current_embed = tf.nn.embedding_lookup(self.Wemb, tf.ones([self.batch_size], dtype=tf.int64))
    #
    #         with tf.variable_scope("LSTM1"):
    #             output1, state1 = self.lstm1(padding, state1)
    #
    #         with tf.variable_scope("LSTM2"):
    #             output2, state2 = self.lstm2(tf.concat([current_embed, output1], 1), state2)
    #
    #         logit_words = tf.nn.xw_plus_b(output2, self.embed_word_W, self.embed_word_b)
    #         max_prob_index = tf.argmax(logit_words, 1)
    #         generated_words.append(max_prob_index)
    #         probs.append(logit_words)
    #
    #         with tf.device("/cpu:0"):
    #             current_embed = tf.nn.embedding_lookup(self.Wemb, max_prob_index)
    #
    #         embeds.append(current_embed)
    #
    #     feats = {
    #         'probs': probs,
    #         'embeds': embeds,
    #         'states': states
    #     }
    #
    #     return word_vectors, generated_words, feats
