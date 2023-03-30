import matplotlib.pyplot as plt
import base64
from io import BytesIO

def graph():
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph1=base64.b64encode(image_png)
    graph1=graph1.decode('utf-8')
    buffer.close()
    return  graph1
def plot(x,y):
    g=graph()
    return graph
