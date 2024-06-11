from processing import process_network_data, generate_legend_html, combine_content
from flask import Flask, render_template
import os


app = Flask(__name__)

@app.route('/')
def index():
    #Procesa los datos de la red
    net = process_network_data()

    #Guarda el gráfico de la red en un archivo HTML temporal
    html_file = 'temp_network.html'
    net.save_graph(html_file)

    # Lee el contenido del archivo HTML generado
    with open(html_file, 'r') as f:
        network_html = f.read()

    # Genera HTML para la leyenda
    legend_html = generate_legend_html()

    #Combina el contenido de la red y la leyenda
    combined_html = combine_content(network_html, legend_html)

    #Borra el archivo temporal
    #os.remove(html_file)

    return combined_html

if __name__ == '__main__':
    app.run(port=3000, debug=True)
