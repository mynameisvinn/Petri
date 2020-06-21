import random
import matplotlib.pyplot as plt

from utils import update_canvass

def simulator(env, canvass, epochs, loop):
    n_rows = env["n_rows"]
    n_cols = env["n_cols"]

    for epoch in range(epochs):        
        loc = random.choice(list(env.keys()))
        if isinstance(loc, tuple):
            element = env[loc]
            element_id = element[0]
            loop[element_id](loc, env)

            if epoch % (epochs / 20) == 0:
                canvass = update_canvass(canvass=canvass, env=env, n_rows=n_rows, n_cols=n_cols)
                plt.figure(figsize = (10, 5))
                plt.imshow(canvass, cmap ='jet')
                plt.colorbar(cmap ='jet')

                # fname = "gif/test_" + str(epoch)
                # plt.savefig(fname)
                # plt.clf()