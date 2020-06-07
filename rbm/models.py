from django.db import models


class RBM():
    def __init__(self, nv, nh):
        self.W = torch.randn(nh, nv) #matrix
        self.a = torch.randn(1, nh) #bias for probability of hidden nodes given visible nodes
        self.b = torch.randn(1, nv) #bias for probability of visible nodes given hidden nodes
    #sampling hidden node according to probability p-h given v - sigmoid activation
    #x- visible neurons v in p_h_given_v
    def sample_h(self, x):
        wx = torch.mm(x, self.W.t())
        activation = wx + self.a.expand_as(wx)
        p_h_given_v = torch.sigmoid(activation)
        return p_h_given_v, torch.bernoulli(p_h_given_v) #bernoulli used to sample probability of hidden node
    #if p_h_given_v for i'th hidden node is 0.7 and some random no is less than 0.7 then we will activate neuron otherwise we won't - explanation for bernoulli sampling
    def sample_v(self, y):
        wy = torch.mm(y, self.W)
        activation = wy + self.b.expand_as(wy)
        p_v_given_h = torch.sigmoid(activation)
        return p_v_given_h, torch.bernoulli(p_v_given_h)
    
    #contrastive divergence - minimizing energy by approximating gradients 
    #gibb sampling - sampling k times the hidden nodes and visible nodes - sample consecutively in chains - gibbs chain
    def train(self, v0, vk, ph0, phk):
        self.W += (torch.mm(v0.t(), ph0) - torch.mm(vk.t(), phk)).t()
        self.b += torch.sum((v0 - vk), 0)
        self.a += torch.sum((ph0 - phk), 0)
        
    def predict(self, x):# x: visible nodes
        _, h = self.sample_h( x)
        _, v = self.sample_v( h)
        return v
# Create your models here.
