from flask import Flask, render_template, request, jsonify
import os
app = Flask(__name__)
port=int(os.environ.get('PORT', 5001))

def validate_inputs(diam_fam, price_fam, diam_med, price_med, border):
    try:
        diam_fam = float(diam_fam)
        price_fam = float(price_fam)
        diam_med = float(diam_med)
        price_med = float(price_med)
        border = float(border)

        if diam_fam <= 0 or price_fam <= 0 or diam_med <= 0 or price_med <= 0:
            return None, "Los diámetros y precios deben ser mayores que cero."
        if border < 0:
            return None, "El ancho del borde no puede ser negativo."
        if border * 2 >= diam_fam or border * 2 >= diam_med:
            return None, "El borde es demasiado ancho para el diámetro de la pizza."

        return (diam_fam, price_fam, diam_med, price_med, border), None
    except ValueError:
        return None, "Por favor, ingrese valores numéricos válidos."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prestar/<isbn>')
def prestar():
    return render_template('index.html')

@app.route('/devolver/<isbn>')
def devolver():
    return render_template('index.html')

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    isbn = request.form.get('isbn')



    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)