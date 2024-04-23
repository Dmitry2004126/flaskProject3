import os
import unittest
from app.models import User, Role
from app import create_app, db




app = create_app('default')

"""
@app.shell_context_processors
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
"""

@app.cli.command('test')
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)