#!/usr/bin/env python3
import sys
from app import app
import atexit

#def exit_handler():
#    print ('Shutting down.')
#    app.shutdown()


#atexit.register(exit_handler)

if __name__ == '__main__':
    sys.exit(app.main(len(sys.argv), sys.argv))
