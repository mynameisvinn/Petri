import random
import matplotlib.pyplot as plt

def update_canvass(canvass, env, n_rows, n_cols, colorkeys):
    """update numpy matrix given world.
    """
    canvass[:] = 0
    for i in range(n_rows):
        for j in range(n_cols):
            loc = (i, j)
            if loc in env.keys():
                element = env[loc][0]
                canvass[i][j] = colorkeys[element]
    return canvass


def simulator(env, canvass, epochs, loop, frames=20, save=False):
    n_rows = env["n_rows"]
    n_cols = env["n_cols"]

    colorkeys = {}
    for i, element in enumerate(loop.keys()):
        colorkeys[element] = i * 2

    for epoch in range(epochs):        
        loc = random.choice(list(env.keys()))
        if isinstance(loc, tuple):
            element = env[loc]
            element_id = element[0]
            loop[element_id](loc, env)

            if epoch % (epochs / frames) == 0:
                canvass = update_canvass(canvass=canvass, env=env, n_rows=n_rows, n_cols=n_cols, colorkeys=colorkeys)
                plt.figure(figsize = (10, 5))
                plt.imshow(canvass, cmap ='jet')
                # plt.colorbar(cmap ='jet')

                if save:
                    fname = "gif/test_" + str(epoch)
                    plt.savefig(fname)
                    plt.clf()