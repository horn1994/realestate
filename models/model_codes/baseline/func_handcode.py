import numpy as np

##############################
#Initializing input parameters

def gen_input_params(data, train_size = 0.8):
    
    Y  = data['price_mil'].to_numpy()
    X = data.drop(columns = ["price_mil", "price_sqm", "id","price_mil_norm", "price_sqm_norm"])
    X = X.to_numpy()
    
    #Train-test split
    Ytrain, Ytest = Y[int(len(Y)*train_size+1):], Y[:int(len(Y)*train_size+1)]
    Xtrain, Xtest = X[int(len(Y)*train_size+1):], X[:int(len(Y)*train_size+1)]
    
    #Data shape and random weight initialization
    D = Xtrain.shape[1]
    M = 100 # number of hidden units

    ## layer 1
    W = np.random.randn(D, M)/np.sqrt(D) #divide by sqare root to normalize the errors (mean 0 std 1)
    b = np.zeros(M)

    ## layer 2
    V = np.random.randn(M) / np.sqrt(M)
    c = 0
    
    return Ytrain, Ytest, Xtrain, Xtest, D, M, W, b, V, c

def sigmoid(a):
    return 1 / (1 + np.exp(-a))

##############################
#ANN functions

#Feed forward
def forward(X, W, b, V, c, activ = "tanh"):
    if activ == "relu":
        Z = np.maximum(X.dot(W) + b, 0) # relu
    if activ == "tanh":
        Z = np.tanh(X.dot(W) + b) # tanh
    if activ == "sigmoid":
        Z = sigmoid(X.dot(W) + b)

    Yhat = Z.dot(V) + c #Note: no functional transofirmation needed for last layer, due to regression not classification
    return Z, Yhat

# Functions for parameter training in backprop.
def derivative_V(Z, Y, Yhat):
    return (Y - Yhat).dot(Z)

def derivative_c(Y, Yhat):
    return (Y - Yhat).sum()

def derivative_W(X, Z, Y, Yhat, V, activ = "tanh"):
    if activ == "relu":
        dZ = np.outer(Y - Yhat, V) * (Z > 0) # relu
    if activ == "tanh":
        dZ = np.outer(Y - Yhat, V) * (1 - Z * Z) # tanh
    if activ == "sigmoid":
        dZ = np.outer(Y - Yhat, V) * Z*(1-Z) # sigmoid
    
    return X.T.dot(dZ)

def derivative_b(Z, Y, Yhat, V, activ = "tanh"):
    if activ == "relu":
        dZ = np.outer(Y - Yhat, V) * (Z > 0) # relu
    if activ == "tanh":
        dZ = np.outer(Y - Yhat, V) * (1 - Z * Z) # tanh
    if activ == "sigmoid":
        dZ = np.outer(Y - Yhat, V) * Z*(1-Z) # sigmoid
        
    return dZ.sum(axis=0)

#Weight update function
def update(X, Z, Y, Yhat, W, b, V, c, learning_rate=1e-7, reg = 1e-8):
    gV = derivative_V(Z, Y, Yhat)
    gc = derivative_c(Y, Yhat)
    gW = derivative_W(X, Z, Y, Yhat, V)
    gb = derivative_b(Z, Y, Yhat, V)

    V += learning_rate*(gV+reg*V)
    c += learning_rate*(gc+reg*c)
    W += learning_rate*(gW+reg*W)
    b += learning_rate*(gb+reg*b)

    return W, b, V, c

#Costs - MSE for regression
def get_cost(Y, Yhat):
    return ((Y - Yhat)**2).mean()