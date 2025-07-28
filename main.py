from config import params
from model import simulate
from animator import animate

def main():
    y, v, leg_force = simulate(params)
    animate(y, params)

if __name__ == "__main__":
    main()