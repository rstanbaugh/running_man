from config import params
from model import simulate
from animator import animate

def main():
    x, y, vx, vy, ke, pe = simulate(params)
    animate(x, y, vx, vy, ke, pe, params)

if __name__ == '__main__':
    main()