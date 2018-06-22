import sys, os, shutil,io, StringIO


def welcome():
    print("Please select the task you would like run:")



welcome()

def test_foo1():
    capturedOutput = StringIO.StringIO()          # Create StringIO object
    sys.stdout = capturedOutput                   #  and redirect stdout.
    welcome()
    sys.stdout = sys.__stdout__                   # Reset redirect.
    assert "Please select the task you would like run:\n" == capturedOutput.getvalue()
