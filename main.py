from workflow import app

print("\n===== Victory AI =====")
print("Escribí tu consulta. Para salir escribí 'salir'.\n")

while True:

    pregunta = input(" Usuario: ")

    if pregunta.lower() == "salir":
        print("\n Victory: ¡Hasta luego!")
        break

    resultado = app.invoke(
        {
            "pregunta": pregunta
        }
    )

    print("\n--------------- Agente Victory ----------------")
    print(resultado["respuesta"])
    print()