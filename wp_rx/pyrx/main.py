import os
import sys

from wp_rx.pyrx.rx_pipe_line import start_pipe_line, completion_handler

if __name__ == '__main__':
    try:
        start_pipe_line(completion_handler)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            is_running = False
            sys.exit(0)
        except SystemExit:
            is_running = False
            os._exit(0)