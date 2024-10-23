# Creazione dell'interfaccia VGA
## Generazione dei segnali di temporizzazione
La prima cosa da fare è quella di creare l'interfaccia VGA per gestire la generazione dei diversi segnali di temporizzazione (so che se ti stai inbattendo in questo argomento questo grafico l'avrai visto alla nasua ma tocca partire dalle basi) \
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
| Visible area | 200  |20    |
| Front porch  | 10   | 1    |
| Sync pulse   | 32  | 3.2   |
| Back porch   | 22   | 2.2  |
| Whole line   | 264 | 26.4  |

<img width="549" alt="H_sync_4" src="https://github.com/user-attachments/assets/60278fac-8f52-4372-b8d7-1bbbec57b3cc">\

Per cui il circuito digitale che andremo ad implementare non è altro che un contatore, prima di passare al codice vhdl , mi è stato molto utile utilizzare un software di simulazione [Digital](https://github.com/hneemann/Digital).\
Quindi in questa prima fase occupiamoci di realizzare il circuito logico, dobbiamo realizzare due contatori uno per il segnale di sincronizzazione verticale e l'altro per quello orizzontale, per qullo orizzontale abbiamo il seguente schema, dovremo contare fino a 264 , in realtà (264 - 1) per cui avremo bisogno di un contatore a 9 bit

<img src="https://github.com/user-attachments/assets/eb6f553a-688c-4d2f-a5c6-97955220caf3" alt="Schematico Contatore Orizzontale" width="500" />\

Mentre per quello verticale , in questo caso dovremo contare fino a 628 , in realtà (628 -1)per cui avremo bisogno di un contatore a 10 bit\

<img src="https://github.com/user-attachments/assets/a4842c9c-7015-4600-b787-9b232f4037a9" alt="Schematico Contatore Verticale" width="500" />\

Il circuito completo\
<img src="https://github.com/user-attachments/assets/de690c3a-53c2-4bcc-a510-9b17ddb1da8a" alt="Schematico Contatore Verticale" width="500" />\

E simulandolo non dovrebbe dare problemi e visualizzare la finestra in cui viene indicata la risoluzione impostata che corrisponde a quella da noi fissata con i segnali di temporizzazione.

## Pronti per generare la prima immagine

A questo punto vediamo se siamo in grado di visualizzare un'immagine presente in memoria, impostiamo il problema nell'ottica di trasferlo su fpga.\

Come immagine di prova non si che utilizzare quella di [Lena](https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FLenna&psig=AOvVaw3KondBdSBRzq3mwXd9Niy-&ust=1729783719933000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCNDWmdTopIkDFQAAAAAdAAAAABAE) immagine impressa nella storia del processing delle immagini. Per prima cosa questa va ridimensionata e poi va passata in uno script python che ci estragga solo i valori delle componenti di colore dei pixel e ci "riquantizzi" ogni componente con 4 bit 

ora io ho a disposizione una scheda de-10 lite la interfaccia VGA consente di avere una risoluzione per i colori fondamentale di 4 bit , per cui in totale ogni pixel può essere memorizzato come una parola di 12 bit.\
Ora supponiamo di avere una memoria di 32 kb questo significa che abbiamo a disposizione 15 linee per gli indirizzi.\
Con questo spazio siamo in grado di memorizzare una immagine di dimensione 100 x 75.\
Ora per accedere agli elementi di memoria dobbiamo combinare il risultato dei due contatori che però andranno divisi per lo stesso fattore che corrisponde all'immagine
-Per l'orizzontale il contatore arriva fino a 200 ma al massimo deve arrivare fino a cento per cui va diviso per 2 ,in binario questo corrisponde a non considera la prima cifra non significativa
-Per la verticale il contatore arriva fino a 600 ma al massimo deve arrivare fino a 75 questo corrisponde a dividire per un vettore 8 ovvero scartare i primi 3 bit significativi.\
Otteniamo questo circuito \

<img src="https://github.com/user-attachments/assets/976d552e-7197-4d4b-8355-a2a79e7e7a59" alt="Schematico Contatore Verticale" width="500" />\

Il risutato è il seguente

<img src="https://github.com/user-attachments/assets/14457dab-3bd2-42d0-a87d-67d9642c7f0e" alt="Schematico Contatore Verticale" width="500" />\


















