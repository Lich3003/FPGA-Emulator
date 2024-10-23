# Creazione dell'interfaccia VGA
## Generazione dei segnali di temporizzazione
La prima cosa da fare è quella di creare l'interfaccia VGA per gestire la generazione dei diversi segnali di temporizzazione (so che se ti stai inbattendo in questo argomento questo grafico l'avrai visto alla nasua ma tocca partire dalle basi) 
<img src="https://github.com/user-attachments/assets/59a6a7bb-b185-42d1-b946-92ecaf77629a" alt="Vga_timing" width="500" />\
Quindi essenzialmente dobbiamo generare questi due segnali di sincronizzazione verticale e orizzontale e per fare ciò dobbiamo rispettare alcuni vincoli temporali che cambiano in funzione della risoluzione dello schermo, un buon riferimento da cui prendere queste informazione è il seguente : [Tiny Vga](http://tinyvga.com/vga-timing).\
Per il momento consideriamo una risoluzione  [800 x 600 ](http://tinyvga.com/vga-timing/800x600@60Hz):
<div style="display: flex; justify-content: center;">

<table>
  <tr>
    <th>Header 1</th>
    <th>Header 2</th>
  </tr>
  <tr>
    <td>Row 1</td>
    <td>Value 1</td>
  </tr>
  <tr>
    <td>Row 2</td>
    <td>Value 2</td>
  </tr>
</table>

<table style="margin-left: 20px;">
  <tr>
    <th>Header A</th>
    <th>Header B</th>
  </tr>
  <tr>
    <td>Row A</td>
    <td>Value A</td>
  </tr>
  <tr>
    <td>Row B</td>
    <td>Value B</td>
  </tr>
</table>

</div>
