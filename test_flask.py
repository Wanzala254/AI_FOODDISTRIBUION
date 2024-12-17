import sys
print(sys.executable)  # This will show which Python you're using
try:
    import flask
    print("Flask version:", flask.__version__)
    print("Flask location:", flask.__file__)
except ImportError as e:
    print("Import Error:", e) 