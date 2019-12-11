from enums import*
import random
import tensorflow as tf
from tensorflow import keras
from keras.layers import Input, Dense
from keras.models import Model, Sequential
from keras.optimizers import Adam
from collections import deque
import numpy as np

class AIsnake:
    def __init__(self, lr=0.0001, discount=0.9, eps=1.0, iterations= 1000):
        self.lr = lr
        self.memory = deque(maxlen=2000)
        self.discount = discount
        self.eps = eps
        self.eps_delta = self.eps / iterations
        self.tau = 0.125
        self.input_size = 16
        self.output_size = 4
        self.model = self.build_model()
        self.target_model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim=self.input_size, activation='sigmoid'))
        model.add(Dense(64, activation="sigmoid"))
        model.add(Dense(64, activation="sigmoid"))
        model.add(Dense(self.output_size))
        model.compile(loss="mean_squared_error",
        optimizer=Adam(lr=self.lr))
        return model
        
    def to_one_hot(self, state):
        one_hot = state.reshape((1,self.input_size))
        return one_hot
    
    def get_next_action(self, state):
        if random.random() < self.eps:
            return random.randint(0,3)
        else:
            state_hoot = self.to_one_hot(state) 
            return np.argmax(self.model.predict(state_hoot))
    
    def remember(self, old_state, action, reward, new_state):
        self.memory.append([old_state, action, reward, new_state])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return
        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            old_state, action, reward, new_state = sample
            old_state_hoot = self.to_one_hot(old_state) 
            new_state_hoot = self.to_one_hot(new_state)
            target = self.target_model.predict(old_state_hoot)
            Q_future = max(self.target_model.predict(new_state_hoot)[0])
            target[0][action] = reward + Q_future * self.discount
            self.model.fit(old_state_hoot, target, epochs=1, verbose=0)
    
    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] *self.tau + target_weights[i]*(1-self.tau)
        self.target_model.set_weights(target_weights)
    def save_model(self,fn):
        self.model.save(fn)
    def update(self, old_state, new_state, action, reward):
        self.remember(old_state, action, reward, new_state)
        self.replay()
        self.target_train()
        if self.eps > 0:
            self.eps = self.eps*0.99






