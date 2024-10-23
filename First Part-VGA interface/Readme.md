# Creazione dell'interfaccia VGA
## Generazione dei segnali di temporizzazione
La prima cosa da fare è quella di creare l'interfaccia VGA per gestire la generazione dei diversi segnali di temporizzazione (so che se ti stai inbattendo in questo argomento questo grafico l'avrai visto alla nasua ma tocca partire dalle basi) 
<img src="https://github.com/user-attachments/assets/59a6a7bb-b185-42d1-b946-92ecaf77629a" alt="Vga_timing" width="500" />\
Quindi essenzialmente dobbiamo generare questi due segnali di sincronizzazione verticale e orizzontale e per fare ciò dobbiamo rispettare alcuni vincoli temporali che cambiano in funzione della risoluzione dello schermo, un buon riferimento da cui prendere queste informazione è il seguente : [Tiny Vga](http://tinyvga.com/vga-timing).\
Per il momento consideriamo una risoluzione  [800 x 600 ](http://tinyvga.com/vga-timing/800x600@60Hz):
| Scanline part  | Pixels | Time µs             |   
| ------------- | ------------- | ------------- | 
| Visible area | 800  |20    |
| Front porch  | 40   | 1    |
| Sync pulse   | 128  | 3.2  |
| Back porch   | 88   | 2.2  |
| Whole line   | 1056 | 26.4 |

| Scanline part  | Pixels | Time µs             |   
| ------------- | ------------- | ------------- | 
| Visible area |  600 |   15.84 |
| Front porch  | 	  1 |  0.0264 |
| Sync pulse   | 	  4 |  0.1056 |
| Back porch   |   23 |  0.6072 |
| Whole line   | 	628 | 16.5792 |

Trovati questi valori il segnale che dobbiamo generare sarà il seguente 
<img width="554" alt="H_sync" src="https://github.com/user-attachments/assets/464af050-0650-4903-ac1b-568227672e85">\
Questo è valido se riusciamo a generare un pixel_clock di 40 MHz nel caso in cui non dovessimo farcela possiamo diminuire la pixel clock a patto di ridurre dello stesso fattore tutte le altre quantità, per esempio riusciamo a genere una frequenza di 10 MHz in questo caso tutti i parametri relativi alla sincronizzazione orizzontale andranno divisi per 4 
| Scanline part  | Pixels | Time µs             |   
| ------------- | ------------- | ------------- | 
| Visible area | 400  |20    |
| Front porch  | 10   | 1    |
| Sync pulse   | 32  | 3.2   |
| Back porch   | 22   | 2.2  |
| Whole line   | 264 | 26.4  |

<img width="549" alt="H_sync_4" src="https://github.com/user-attachments/assets/60278fac-8f52-4372-b8d7-1bbbec57b3cc">\

Per cui il circuito digitale che andremo ad implementare non è altro che un contatore, prima di passare al codice vhdl , mi è stato molto utile utilizzare un software di simulazione [Digital](https://github.com/hneemann/Digital))

