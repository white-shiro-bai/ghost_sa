from flask import Flask
from werkzeug.local import Local

app = Flask(__name__)

# Using thread local storage
thread_local = Local()

# Set dictionary in thread local storage
def set_dict_in_thread_local(my_dict):
    thread_local.my_dict = my_dict

# Using LocalProxy to create a proxy object
from werkzeug.local import LocalProxy

my_dict_proxy = LocalProxy(lambda: getattr(thread_local, 'my_dict', {}))

aaa = {'a': 123, 'b': 456}

@app.route('/')
def index():
    # Set dictionary in thread local storage during request handling
    
    set_dict_in_thread_local({'a': 123, 'b': 456})

    # Access and modify 'b' in the dictionary using LocalProxy during request handling
    aaa['b'] = 789

    # Display the modified dictionary
    return f'Modified dictionary in thread local storage: {aaa}'

@app.route('/a')
def index2():
    # Set dictionary in thread local storage during request handling
    # set_dict_in_thread_local({'a': 123, 'b': 456})

    # Access and modify 'b' in the dictionary using LocalProxy during request handling
    aaa['b'] = 987

    # Display the modified dictionary
    return f'Modified dictionary in thread local storage: {aaa}'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
