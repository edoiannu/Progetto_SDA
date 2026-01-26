import random

# converte una stringa in una rappresentazione binaria, dove ogni carattere è rappresentato da 8 bit come lista di numeri
def string_to_binary(s):
    # per ogni carattere 'c' nella stringa, ottiene il codice ASCII con ord(c),
    # format(..., '08b') lo converte in binario con 8 bit con padding di zeri a sinistra, e crea una lista di interi
    # il ciclo più esterno (il primo) itera sui caratteri della stringa
    # il ciclo interno (il secondo) itera sui bit della stringa binaria di quel carattere e li converte in interi
    return [int(b) for c in s for b in format(ord(c), '08b')]

# converte una lista di bit (numeri 0 o 1) in una stringa alfanumerica
def binary_to_string(binary_list):
    # lista per raccogliere i caratteri convertiti
    result = []
    # itera sulla lista binaria a passi di 8 bit
    for i in range(0, len(binary_list), 8):
        # estrae un blocco di 8 bit
        byte = binary_list[i:i+8]
        # se il blocco ha esattamente 8 bit, lo converte
        if len(byte) == 8:
            # converte la lista in stringa binaria, poi in intero, poi in carattere ASCII
            byte_str = ''.join(str(b) for b in byte)
            char = chr(int(byte_str, 2))
            result.append(char)
    # unisce tutti i caratteri in una stringa
    return ''.join(result)

# funzione che calcola le posizioni dei bit di parità
# prende in input la lunghezza del messaggio
def parity_bits(k):
    r = 0
    while (2**r) < (k + r + 1):
        r += 1
    return [2**i for i in range(r)]

# funzione che calcola le posizioni dei bit riservati al messaggio
# prende in input la lunghezza del messaggio
def message_bits(k):
    r = len(parity_bits(k)) # numero dei bit di parità
    data_bits = []
    for i in range(1, k + r + 1):   # l'elemento con indice 0 è riservato al bit di parità globale
        # verifica se 'i' non è una potenza di 2 usando l'operatore bitwise AND (&)
        # se i è potenza di 2 (es. 1, 2, 4, 8), 'i & (i-1)' è sempre 0
        if (i & (i - 1)) != 0:
            data_bits.append(i)
    return data_bits

# funzione che calcola la sindrome del blocco ricevuto
def sindrome(block):
    s = 0
    for i in range(1, len(block)):
        if block[i] == 1:
            s ^= i
    return s

# funzione che calcola il bit di parità globale
def global_parity_check(block):
    return sum(block) % 2

# funzione che rileva e corregge gli errori nel blocco ricevuto
def detect_errors(block):
    s = sindrome(block) # calcola la sindrome del blocco ricevuto
    if s == 0:
        return 0  # nessun errore rilevato
    else:
        block[s] ^= 1  # Corregge l'errore
        if global_parity_check(block) == 0:
            return block  # errore singolo corretto
        else:
            return 1  # errore multiplo rilevato, chiediamo di reinviare il blocco

# 'with' è un "gestore di contesto": garantisce che il file venga chiuso automaticamente non appena finiamo di leggere, evitando sprechi di memoria o errori di sistema
# Questo comando apre il file "Alice.txt" in modalità lettura
with open("Alice.txt", "r") as file:
    # Legge tutto il contenuto del file e rimuove eventuali spazi bianchi iniziali/finali
    input_str = file.read().strip()

# Converte la stringa letta in rappresentazione binaria
binary_message = string_to_binary(input_str)

k = 4 # lunghezza del messaggio in bit per ogni blocco
r = len(parity_bits(k))  # numero dei bit di parità
n = 1 + k + r  # lunghezza del blocco (incluso il bit di parità globale)

# Dividi la lista "binary_message" in sottoliste di 4 bit ciascuna
data = [binary_message[i:i+4] for i in range(0, len(binary_message), k)]

received_data = []

for i in range(len(data)):
    # completiamo il messaggio i-esimo inserendo i bit di parità
    message = data[i]
    block = [0] * (1 + k + r) # pre-alloca una lista della lunghezza desiderata riempiendola con zeri
    # Posiziona i bit di dati nelle posizioni non potenza di 2
    data_idx = 0
    for i in message_bits(k):
        block[i] = message[data_idx]
        data_idx += 1
    for i in parity_bits(k):
        # L'operatore '<<' (Left Shift) sposta i bit a sinistra: 1 << p equivale a 2^p
        # parity_pos = (1 << p)  # posizione 1-based della parità (1, 2, 4, ...)
        # print("Calcolo bit di parità per la posizione", i)
        parity = 0
        for j in range(1, k + r + 1):
            if j & i:  # Se il risultato dell'AND è diverso da zero, significa che la posizione 'j' è controllata dal bit di parità corrente
                # print("Il bit di parità alla posizione", i, "controlla il bit in posizione", j, "con valore", message[j])
                parity ^= block[j]  # il comando '^' è lo XOR per calcolare la parità
        block[i] = parity
        # print("Bit di parità calcolato per la posizione", i, ":", parity)
    # calcolo del bit di parità globale
    overall_parity = sum(block) % 2
    block[0] = overall_parity
    # introduciamo degli errori casuali
    p = 0.05  # probabilità di errore (bit flip)
    send = 1
    appo = block.copy() # copia del blocco originale per il reinvio in caso di errore multiplo
    while send == 1:
        for i in range(n):
            if random.random() < p:
                # Effettua il bit flip
                if appo[i] == 0:
                    appo[i] = 1
                else:
                    appo[i] = 0
        send = detect_errors(appo)
    received_data.extend([appo[i] for i in range(1, n) if i not in parity_bits(k)])  # esclude tutti i bit di parità

# messaggio che riceve Bob scritto su file
with open("Bob.txt", "w") as file_output:
    file_output.write(binary_to_string(received_data))

# Manda a video la stringa convertita indietro
# print("Converted back to string:", original_back)