from app import app


@app.route('/')
def index():
    return "Hello world and Jimmie."


if __name__ == '__main__':
    app.run(port=5002, debug=True)
