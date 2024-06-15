class Auto():
    def __init__(self, marca, modelo, color):
        self.marca = marca
        self.modelo = modelo
        self.color = color

    def arrancar(self):
         print("el auto arranco")


AutoUno = Auto("Fiat600", 1960, "Rojo" )

AutoUno.arrancar()

# Herencia
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola , me llamo {self.nombre} y mi edad {self.edad}")


class Empleado(Persona):
    def __init__(self, nombre, edad, puesto):
        super().__init__(nombre, edad)
        self.puesto = puesto
    
    def mostrar_empleado(self):
        print(f"Soy {self.nombre} y trabajo como {self.puesto} ")

empleado_uno =  Empleado("Carlos", 28, "Desarrollador")
empleado_uno.mostrar_empleado()

# Encapsulamiento
class CuentaBancaria():
    def __init__(self, titular, balance):
         self.titular = titular
         self.__balance = balance

    def depositar(self, cantidad):
        if cantidad > 0:
            self.__balance += cantidad
            print(f"Depósito exitoso. Nuevo balance: {self.__balance}")
        else:
            print("La cantidad debe ser positiva.")

    def retirar(self, cantidad):
        if 0 < cantidad <= self.__balance:
            self.__balance -= cantidad
            print(f"Retiro exitoso. Nuevo balance: {self.__balance}")
        else:
            print("Fondos insuficientes o cantidad inválida.")
        
cuenta_UNO = CuentaBancaria("Pedro", 10000)

cuenta_UNO.depositar(50000)
cuenta_UNO.retirar(10000)

print(cuenta_UNO.__balance)



