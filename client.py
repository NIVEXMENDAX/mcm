import socket
import threading

SERVER_IP = "101.177.102.102"
PORT = 5555
IS_ADMIN = False  # Set this to True in the admin client version

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                print("\n[ERROR] Server disconnected.")
                break
            print(f"\n{message}")
        except Exception as e:
            print(f"\n[ERROR] Error receiving message: {e}")
            break

# Function to send messages to the server
def send_message(client_socket, message):
    try:
        if message.lower() == "exit":
            client_socket.close()
            return False
        else:
            client_socket.send(message.encode("utf-8"))
            return True
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")
        return False

# Main client function
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
        print("[CONNECTED] Successfully connected to the server.")
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        return

    # Admin mode check
    if IS_ADMIN:
        print("[INFO] Admin mode enabled.")
        client.send("admin".encode("utf-8"))
        password_prompt = client.recv(1024).decode("utf-8")
        print(password_prompt)
        password = input("Enter admin password: ").strip()  # User will input the password
        client.send(password.encode("utf-8"))
        admin_response = client.recv(1024).decode("utf-8")
        print(admin_response)

        if "wrong password" in admin_response.lower():
            print("[ERROR] Admin login failed.")
            client.close()
            return
    else:
        username = input("Enter your username: ").strip()
        client.send(username.encode("utf-8"))

    # Start receiving messages in a separate thread
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    print("[INFO] Type messages normally. Use commands like '/list', '/history', '/clear', etc.")

    while True:
        message = input("You: ")
        if not send_message(client, message):
            break

if __name__ == "__main__":
    start_client()
