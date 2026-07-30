# %%
# # Operadores ternarios
# variable = "value" if condition else "other_value"

orders = [
    {"id": 101, "total": 45, "status": "paid"},
    {"id": 102, "total": 5, "status": "pending"},
    {"id": 103, "total": 120, "status": "paid"},
]

# %%

for order in orders:
    action = "ship" if order["status"] == "paid" else "hold"
    print(order["id"], action)

# %%

for order in orders:
    if order["status"] == "paid":
        action = "ship"
    else:
        action = "hold"
    print(order["id"], action)

# %%

http_request = 403

match http_request:
    case 200 | 201 | 202:
        print("Correct response")
    case 300 | 301 | 302:
        print("Redirect")
    case 400 | 401 | 403:
        print("Client error")
    case 500 | 501 | 502:
        print("Server error")

# %%

http_request = 500

if http_request in (200, 201, 202):
    print("Correct response")
elif http_request == 300 or http_request == 301 or http_request == 302:
    print("Redirect")
elif http_request in (400, 401, 403):
    print("Client error")
elif http_request in (500, 501, 502):
    print("Server error")


# %%

error_message = "server internal error"

if message := error_message.startswith("server"):
    print(f"problemas en el servidor \n {message}")

# %%

error_message = "server internal error"

message = error_message.startswith("server")

if message:
    print(f"problemas en el servidor \n {message}")

# %%

error_message = "server internal error"

if error_message.startswith("server"):
    print(f"problemas en el servidor \n {error_message.startswith("server")}")

# %%

error_message = "server internal error"

while message := error_message.startswith("server"):
    print(f"problemas en el servidor \n {message}")
    error_message = ""


# %%
mi_lista = []
for numero in range(100_000):
    if numero % 2 == 0:
        mi_lista.append(numero ** 2)

print(len(mi_lista))

# %%

mi_lista_2 = [ numero ** 2 for numero in range(100_000) if numero % 2 == 0 ]
print(len(mi_lista_2))
print(mi_lista_2[:5])