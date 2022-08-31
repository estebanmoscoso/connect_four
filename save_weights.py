from neural_lib import *

def salvar_pesos():
#print(N_HID*N_IN)
    with open('net_hid_weights.txt', 'w') as f:
        for k in range(N_HID):
            for i in range(N_IN):
                if k == (N_HID - 1) and i == (N_IN - 1):
                    f.write(f"{hidden_layer.weights[k][i]}")
                else:
                    f.write(f"{hidden_layer.weights[k][i]}\n")
    f.close()


    #print(N_HID*N_OUT)
    with open('net_out_weights.txt', 'w') as f:
        for k in range(N_OUT):
            for i in range(N_HID):
                if k == (N_OUT - 1) and i == (N_HID - 1):
                    f.write(f"{out_layer.weights[k][i]}")
                else:
                    f.write(f"{out_layer.weights[k][i]}\n")
    f.close()



def cargar_pesos():
    with open('net_hid_weights.txt', 'r') as f:
        l = f.readlines()
        count = 0
        for k in range(N_HID):
            for i in range(N_IN):
                hidden_layer.weights[k][i] = float(l[count])
                count += 1
    f.close()

    #print(N_HID*N_OUT)
    with open('net_out_weights.txt', 'r') as f:
        l = f.readlines()
        count = 0
        for k in range(N_OUT):
            for i in range(N_HID):
                out_layer.weights[k][i] = float(l[count])
                count += 1
    f.close()

