from Subsystem_Libraries.Simple_Socket import Coms
from Subsystem_Libraries.Handheld_Controls import Xbox_Controller as xbc
import time


server = Coms.SocketServer("0.0.0.0", 55555)
controller = xbc.setUpController()
while True:
    try:
        ljh, ljv, rjh, rjv, lt, rt, A, B, X, Y, lb, rb, back, start, ljb, rjb, dpl, dpr, dpu, dpd = xbc.getInput(controller)
        Coms.send_data(str(A)+str(B), ("localhost", 44444))
        if server.get_data() is not None:
            print(server.get_data())
            server.clear_data()
        time.sleep(0.1)

    except KeyboardInterrupt:
        server.close()
        break
