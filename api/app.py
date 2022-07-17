from flask import Flask, jsonify
from consumeApiComputerVision import consumeApiComputerVision 

app = Flask(__name__)

@app.route('/cv')
def consume():
    placa, contorno = consumeApiComputerVision()
    return jsonify({"placa" : placa, "contorno" : contorno})


if __name__ == '__main__':
    app.run(debug=True)