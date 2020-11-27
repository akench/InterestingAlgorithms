import random
import matplotlib.pyplot as plt
import numpy as np


def gen_data(num_samples):
    data = []
    for _ in range(num_samples):
        x = np.array([1, random.uniform(-10, 10)])
        y = 2*x[1] + 5

        data.append((x, y + random.gauss(0, 2)))
    return data


def plot_data(data, w, name):
    plt.clf()

    # plot regression line
    x = np.linspace(-10, 10, 2)
    xvector = np.array([ [1, n] for n in x ])

    y = np.dot(xvector, w)
    plt.plot(x, y, '-r', label='model')
    
    # plot data points
    xs = []
    ys = []
    for x,y in data:
        xs.append(x[1])
        ys.append(y)
    plt.scatter(xs, ys)
    plt.grid()
    plt.savefig('out/' + name + '.jpg')


def plot_loss_gradient(data):
    plt.clf()

    size = 30
    x = np.linspace(-100, 100, size)
    y = np.linspace(-10, 10, size)

    X, Y = np.meshgrid(x, y)


    Z = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(mse_loss(data, np.array([X[i, j], Y[i, j]])))
        Z.append(row)
    Z = np.array(Z)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z, 100)
    ax.set_xlabel('bias')
    ax.set_ylabel('slope')
    ax.set_zlabel('error')
    fig.savefig('error_gradient.jpg')

    min_index = np.unravel_index(Z.argmin(), Z.shape)
    print('error of', Z[min_index], 'at coords: (', X[min_index], Y[min_index], ')')

def train(data, alpha):
    w = np.array([0,0])
    for iter in range(7001):
        if iter % 1000 == 0:
            plot_data(data, w, str(iter))
            print('iter:', iter)
            print('weights:', list(w))
            print('MSE:', mse_loss(data, w))
            print()

        loss_gradient = sum_loss_gradients(data, w)
        # x, y = random.sample(data, 1)[0]
        # loss_gradient = get_loss_gradient(x, y, w)
        w = w - alpha*loss_gradient

    return w


def sum_loss_gradients(data, w):
    gradients = [get_loss_gradient(x, y, w) for x, y in data]
    return sum(gradients)

def get_loss_gradient(x, y, w):
    # loss = (model(w,x) - y) ** 2
    # dloss/dw =  2(model(w,x) - y) * x
    # gradient of loss wrt. all weights =  2(model(w,x) - y) * xvector
    #                                       scalar      *      vector    ==> vector gradient
    scalar = 2 * (np.dot(w, x) - y)
    return scalar * x


def mse_loss(data, w):
    sum = 0
    for x, y in data:
        loss = (np.dot(w, x) - y) ** 2
        sum += loss
    return sum / len(data)


if __name__ == '__main__':
    """
    given: some data points
    """
    data = gen_data(100)
    plot_loss_gradient(data)

    w = train(data, 0.00001)
    plot_data(data, w, 'final')
    print('final loss', mse_loss(data, w))
