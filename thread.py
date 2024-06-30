#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      asus
#
# Created:     29-06-2024
# Copyright:   (c) asus 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import socket
import threading
import random
import math
import base64

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True

def generate_prime(min_val, max_val):
    prime = random.randint(min_val, max_val)
    while not is_prime(prime):
        prime = random.randint(min_val, max_val)
    return prime

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Modular inverse (private key) doesn't exist")



def generate_keys():
    p = generate_prime(100, 300)
    q = generate_prime(100, 300)
    while p == q:
        q = generate_prime(100, 300)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while math.gcd(e, phi) != 1:
        e += 2
    d = mod_inverse(e, phi)
    return (n, e), (n, d)

def rsa_encrypt(message, key):
    n, e = key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def rsa_decrypt(encrypted_message, key):
    n, d = key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message

def serialize_key(key):
    return f"{key[0]}|{key[1]}"

def deserialize_key(key_str):
    try:
        n, exp = key_str.split('|')
        return int(n), int(exp)
    except ValueError:
        print(f"Error deserializing key: {key_str}")
        return None

def send_message(c, public_key):
    while True:
        message = input("")
        encrypted_message = rsa_encrypt(message, public_key)
        c.send(str(encrypted_message).encode('utf-8'))
        print("You: " + message)

def receive_message1(c, private_key):
    while True:
        encrypted_message = c.recv(1024).decode('utf-8')
        encrypted_message = eval(encrypted_message)
        message = rsa_decrypt(encrypted_message, private_key)
        print("Rakin: " + message)
        
def receive_message2(c, private_key):
    while True:
        encrypted_message = c.recv(1024).decode('utf-8')
        encrypted_message = eval(encrypted_message)
        message = rsa_decrypt(encrypted_message, private_key)
        print("Nasif: " + message)

choice = input("Host(1) or connect(2)? ")

public_key, private_key = generate_keys()

host = socket.gethostbyname(socket.gethostname())
port = 1430
# same port for client and server
if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Server listening...")
    client, _ = server.accept()
    print("Client connected!")

    # Send server's public key to client
    serialized_key = serialize_key(public_key)
    print(f"Sending public key: {serialized_key}")
    client.send(serialized_key.encode('utf-8'))
    
    # Receive client's public key
    client_key_str = client.recv(1024).decode('utf-8')
    print(f"Received client public key: {client_key_str}")
    partner_public_key = deserialize_key(client_key_str)

    threading.Thread(target=send_message, args=(client, partner_public_key)).start()
    threading.Thread(target=receive_message1, args=(client, private_key)).start()

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Connected to server!")

    # Receive server's public key
    server_key_str = client.recv(1024).decode('utf-8')
    print(f"Received server public key: {server_key_str}")
    partner_public_key = deserialize_key(server_key_str)
    
    # Send client's public key to server
    serialized_key = serialize_key(public_key)
    print(f"Sending public key: {serialized_key}")
    client.send(serialized_key.encode('utf-8'))

    threading.Thread(target=send_message, args=(client, partner_public_key)).start()
    threading.Thread(target=receive_message2, args=(client, private_key)).start()

else:
    exit()
