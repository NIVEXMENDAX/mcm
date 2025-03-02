import socket
import threading

# Client configuration: connect to the encryption server
SERVER_IP = "101.177.102.102"
PORT = 5556  # Change this to the port the middleman server is listening on

# Shared secret key (must match what the encryption server uses)
SECRET_KEY = b"supersecretkey"

# Simple XOR encryption/decryption function
def xor_encrypt_decrypt(data, key):
    key_length = len(key)
    return bytes([data[i] ^ key[i % key_length] for i in range(len(data))])

# Function to receive messages from the server and decrypt them
def receive_messages(client_socket):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print("\n[ERROR] Server disconnected.")
                break
            # Decrypt the received data
            decrypted_bytes = xor_encrypt_decrypt(encrypted_message, SECRET_KEY)
            # Decode to string (replace errors if any)
            decrypted_message = decrypted_bytes.decode("utf-8", errors="replace")
            print(f"\n{decrypted_message}")
        except Exception as e:
            print(f"\n[ERROR] Error receiving message: {e}")
            break

# Function to encrypt and send a message to the server
def send_message(client_socket, message):
    try:
        if message.lower() == "exit":
            client_socket.close()
            return False
        else:
            # Encrypt the message before sending
            encrypted_message = xor_encrypt_decrypt(message.encode(), SECRET_KEY)
            client_socket.send(encrypted_message)
            return True
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")
        return False

# Main client function
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
        print("[CONNECTED] Successfully connected to the encryption server.")
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        return

    # Start the receiving thread
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    print("[INFO] Type messages normally. Type 'exit' to quit.")
    while True:
        message = input("You: ")
        if not send_message(client, message):
            break

if __name__ == "__main__":
    start_client()
