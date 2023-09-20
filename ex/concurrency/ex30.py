import sys
import tty
import termios
from loguru import logger


def confirm_exit():
    confirmation = input("Are you sure you want to exit? (y/n)")
    if confirmation.lower() == "y":
        print("\n")
        sys.exit()

def exit_on_alt_q():
    # save terminal settings
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())

        while True:
            # read keypress
            key = ord(sys.stdin.read(1))
            logger.info(f"key: {key} pressed.")
            if key == 17: # ctrl-q key
                sys.exit()
            if key == 27: # escape key
                # read next two bytes to check for alt-q
                key = ord(sys.stdin.read(1))
                logger.info(f"key: {key} pressed.")
                # if key == 91: # left bracket
                #     key = ord(sys.stdin.read(1))
                #     logger.info(f"key: {key} pressed.")
                if key == 113: # q key
                    sys.exit()
    except KeyboardInterrupt: # ctrl-c
        confirm_exit()
    finally:
        # restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

exit_on_alt_q()
