from flask import Flask, request, render_template
from experta import *

app = Flask(__name__)

class DiagnosticoMedico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultados = []  # Lista para almacenar los resultados del diagnóstico

    @Rule(Fact(action='diagnostico'), 
          NOT(Fact(sintoma=W())), 
          salience=10)
    def preguntar_sintomas(self):
        sintomas = request.form.getlist('sintomas')
        if sintomas:  # Verificar si hay síntomas seleccionados
            for sintoma in sintomas:
                self.declare(Fact(sintoma=sintoma))
            self.declare(Fact(action='diagnostico'))  # Asegurarse de que se declare la acción
        else:
            self.declare(Fact(sintoma=None))  # Declarar un hecho nulo si no hay síntomas

    @Rule(Fact(action='diagnostico'), Fact(sintoma='fiebre'))
    def diagnostico_fiebre(self):
        self.resultados.append("Diagnóstico: Puede tener fiebre.")

    @Rule(Fact(action='diagnostico'), Fact(sintoma='tos'))
    def diagnostico_tos(self):
        self.resultados.append("Diagnóstico: Puede tener tos.")

    # Agrega más reglas según sea necesario

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        engine = DiagnosticoMedico()
        engine.reset()  # Reiniciar el motor de reglas
        engine.declare(Fact(action='diagnostico'))  # Declarar la acción de diagnóstico
        engine.run()  # Ejecutar el motor de reglas
        resultados = engine.resultados  # Obtener los resultados del diagnóstico
        return render_template('resultado.html', resultados=resultados)  # Pasar resultados a la plantilla
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
