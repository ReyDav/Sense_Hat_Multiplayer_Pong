import client_1
import client_emu
import threading

if __name__ == "__main__":
    c = client_1.Game()
    e = client_emu.Game()
    
    client = threading.Thread(target=c.run)
    emu = threading.Thread(target=e.run)
    
    client.start()
    emu.start()



