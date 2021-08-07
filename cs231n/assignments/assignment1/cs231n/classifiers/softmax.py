from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    
    for i in range(num_train):
        scores = X[i].dot(W)
        exp_scores = np.exp(scores)
        
        softmax_value = exp_scores/np.sum(exp_scores)
  
        loss -= np.log(softmax_value[y[i]])

        gradient = softmax_value.reshape(1,-1)
        gradient[0, y[i]] += -1

        dW += X[i].reshape(-1,1).dot(gradient)

    loss /= num_train
    loss += reg * np.sum(W**2)

    dW /= num_train
    dW += 2 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]

    scores = X.dot(W)
    scores = scores - np.max(scores, keepdims=True)

    exp_scores = np.exp(scores)
    # axis=1 => sum by each row
    sum_exp_scores = exp_scores.sum(axis=1, keepdims=True)
    softmax_value = exp_scores/sum_exp_scores

    # np.arange(n) -> [0, ..., n]
    loss = np.sum(-np.log(softmax_value[np.arange(num_train), y]) )

    softmax_value[np.arange(num_train), y] -= 1
    dW = (X.T).dot(softmax_value)

    loss /= num_train
    loss += reg * np.sum(W ** 2)

    dW /= num_train
    dW += reg * 2 * W 

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
