from config import params
from model import simulate
from animator import animate

def main():
    x, y, vx, vy, leg_contact = simulate(params)
    animate(x, y, leg_contact, params)

if __name__ == "__main__":
    main()