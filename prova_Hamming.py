import random

message = [0, 0, 1, 1]  # esempio di messaggio da inviare

print("Messaggio da inviare:", message)

k = len(message)  # lunghezza del messaggio

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

r = len(parity_bits(k))  # numero dei bit di parità

# Crea la lista codificata con posizioni per dati e parità
block = [0] * (1 + k + r) # comando che pre-alloca una lista della lunghezza desiderata riempiendola con un valore predefinito (in questo caso lo zero)

n = len(block)  # lunghezza del blocco

# Posiziona i bit di dati nelle posizioni non potenza di 2 (1-based)
data_idx = 0
for i in message_bits(k):
    block[i] = message[data_idx]
    data_idx += 1

print("Blocco messaggio + bit di parità settati a 0:", block)

# Calcola i bit di parità
for i in parity_bits(k):
    # L'operatore '<<' (Left Shift) sposta i bit a sinistra: 1 << p equivale a 2^p
    # parity_pos = (1 << p)  # posizione 1-based della parità (1, 2, 4, ...)
    print("Calcolo bit di parità per la posizione", i)
    parity = 0
    for j in range(1, k + r + 1):
        if j & i:  # Se il risultato dell'AND è diverso da zero, significa che la posizione 'j' è controllata dal bit di parità corrente
            print("Il bit di parità alla posizione", i, "controlla il bit in posizione", j, "con valore", block[j])
            parity ^= block[j]  # il comando '^' è lo XOR per calcolare la parità
    block[i] = parity
    print("Bit di parità calcolato per la posizione", i, ":", parity)

print("Blocco senza bit di parità globale:", block)

# calcolo del bit di parità globale
overall_parity = sum(block) % 2
block[0] = overall_parity

print("Blocco finale:", block)

print("Sindrome calcolata sul blocco inviato (prima di introdurre errori):", sindrome(block))

# introduciamo degli errori casuali

p = 0.1  # probabilità di errore (bit flip)

for i in range(n):
    if random.random() < p:
        # Effettua il bit flip
        if block[i] == 0:
            block[i] = 1
        else:
            block[i] = 0

print("Blocco ricevuto (con possibili errori):", block)

# rilevamento e correzione degli errori

print("Sindrome calcolata sul blocco ricevuto (dopo possibili errori):", sindrome(block))

# funzione che calcola il bit di parità globale
def global_parity_check(block):
    return sum(block) % 2

# funzione che rileva e corregge gli errori nel blocco ricevuto
def correct_errors(block):
    s = sindrome(block) # calcola la sindrome del blocco ricevuto
    # overall_parity = global_parity_check(block) # calcola la parità globale del blocco ricevuto
    # se nè la sindrome nè la parità globale indicano un errore, il blocco è corretto
    # if s == 0 and overall_parity == 0:
        # print("Nessun errore rilevato.")
    # se la sindrome indica un errore in una posizione specifica e la parità globale indica un errore, abbiamo un errore singolo che può essere corretto
    if s != 0 and overall_parity == 1:
        # print("Errore singolo rilevato in posizione", s, ". Correzione in corso...")
        block[s] ^= 1  # Corregge l'errore
        # print("Blocco corretto:", block)
    # se la sindrome indica nessun errore ma la parità globale indica un errore, l'errore è sul bit di parità globale (il messaggio è corretto)
    # elif s == 0 and overall_parity == 1:
        # print("Errore rivelato sul bit di parità globale.")
    # se sia la sindrome che la parità globale indicano un errore, abbiamo un errore multiplo che non può essere corretto. Il messaggio deve essere reinviato
    else:
        print("Errore multiplo rilevato. Non è possibile correggerlo. Reinviare il blocco.")
    return block

print(correct_errors(block))