import random
import matplotlib.pyplot as plt
import numpy as np

def gen_data(num_samples):
    data = []
    for _ in range(num_samples):
        x = random.uniform(-10, 10)
        y = fn(x)

        data.append((x, y + random.gauss(0, 0)))
    return data


def plot_data(data, w, name):
    plt.clf()

    plt.xlim(-12, 12)
    plt.ylim(-20, 25)

    x = np.linspace(-10, 10, 2)
    y = model(w, x)
    plt.plot(x, y, '-r', label='model')
    

    xs = []
    ys = []
    for x,y in data:
        xs.append(x)
        ys.append(y)
    plt.scatter(xs, ys)
    plt.grid()
    plt.savefig(name + '.jpg')


def fn(x):
    return 2*x + 5


def model(w, x):
    b, m = w
    return b + m*x


def train(data, alpha):
    w = [random.uniform(-1, 1), random.uniform(-1, 1)]
    print(w)

    for iter in range(10000):

        if iter % 1000 == 0:
            plot_data(data, w, str(iter))

        loss_gradient = sum_loss_gradients(data, w)
        # x, y = random.sample(data, 1)[0]
        # loss_gradient = get_loss_gradient(x, y, w)

        new_w = []
        for i in range(len(w)):
            new_w.append(w[i] - alpha*loss_gradient[i])
        w = new_w

        if iter % 10 == 0:
            print('loss gradient', loss_gradient)
            print('new weights', w)
            print()

    return w


def sum_loss_gradients(data, w):
    gradients = [get_loss_gradient(x, y, w) for x, y in data]
    return list(map(sum, zip(*gradients)))

def get_loss_gradient(x, y, w):
    # loss = (model(w,x) - y) ** 2
    # dloss/dw =  2(model(w,x) - y) * x
    # gradient of loss wrt. all weights =  2(model(w,x) - y) * xvector
    #                                       scalar      *      vector    ==> vector gradient
    xvector = [1, x]
    scalar = 2 * (model(w,x) - y)
    
    test = [scalar * d for d in xvector]
    return test

def mse_loss(data, w):
    sum = 0
    for x, y in data:
        loss = (model(w, x) - y) ** 2
        sum += loss
    return sum / len(data)

if __name__ == '__main__':
    """
    given: some data points
    """
    data = gen_data(100)
    w = train(data, 0.00001)
    plot_data(data, w, 'final')
    print('total loss', mse_loss(data, w))

