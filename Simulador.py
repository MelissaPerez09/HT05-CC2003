# Nombre: Emily ELvia Melissa Perez Alarcon
# Carnet: 21385
# Curso: Algoritmos y estructuras de datos
# Nombre del programa: Calculadora.java
# Creacion: 11/03/2022
# Ultima modificacion: 13/03/2022

#importa las librerias
import simpy
import random
import statistics

#realiza las comparaciones entre los procesos
random.seed(10)

#lista que guardara todos los tiempos de ejecucion
tiempoV = []
#define el numero de proceso
numProcesos = 25
#establece el numero de procesadores
procesadores = 1
#establece el numero de instrucciones
subprocesos = 3
#establece el tamanio de la RAM
capacidad = 200
#velocidad a la que los procesos son recibidos
intervalos = 5

#comienza a implementar la funcion
def proceso(name, env, cpu, wait, RAM):
    #tiempo en que recive la instruccion
    tiempoRecibido = env.now
    #la RAM es requerida
    cantRAM = random.randint(1, 10)
    #numero de pasos en la instruccion
    instruccion = random.randint(1, 10)

    #imprime la informacion 
    print('%s tiempo atendido %f, cantidad de RAM %d, instrucciones %d' %
          (name, tiempoRecibido, cantRAM, instruccion))

    #asigna a la RAM una instruccion si esta disponible
    with RAM.get(cantRAM) as asigarRAM:
        yield asigarRAM
        yield env.timeout(1)
        #imprime que la instruccion esta lista
        print("%s READY" % name)

        #ciclo que da instruccion al CPU mientras se ejecuta la anterior
        while instruccion > 0:
            #imprime que la instruccion se esta corriendo
            print('%s RUNNING' % name)
            #se asigna la instruccion al CPU
            with cpu.request() as turn:
                yield turn
                #si la instruccion es menor al subproceso, la saca mas rapido
                if instruccion <= subprocesos:
                    yield env.timeout(1)
                    #la instruccion es terminada
                    instruccion = 0
                #si la instruccion tiene mas de 3 instrucciones, ejecuta solo 3
                else:
                    yield env.timeout(1)
                    instruccion -= subprocesos
                    #revisa las operaciones
                    if random.randint(1, 2) == 1:
                        #ejecuta las operaciones
                        with wait.request() as operation:
                            yield operation
                            print("%s ESPERANDO" % name)
                            yield env.timeout(1)

        #retorna la cantidad de RAM utilizada
        with RAM.put(cantRAM) as returnRAM:
            yield env.timeout(1)
            yield returnRAM

    #guarda el tiempo recibido
    totalTime = env.now - tiempoRecibido
    print('%s TERMINADO en %f' % (name, totalTime))
    tiempoV.append(totalTime)
    print()


#condiciones simpy para ejecutar el programa
env = simpy.Environment()
RAM = simpy.Container(env, init=capacidad, capacity=capacidad)
CPU = simpy.Resource(env, capacity=procesadores)
WAITING = simpy.Resource(env, capacity=1)

#ejecuta todo el proceso
def main(environment, ram, cpu, waiting):
    for i in range(numProcesos):
        env.process(proceso("PROCESO %d" % i, environment, cpu, waiting, ram))
        yield env.timeout(random.expovariate(1.0 / intervalos))


#ejecuta el ambiente simpy
env.process(main(env, RAM, CPU, WAITING))
env.run()

#imprime la informacion final
print("El promedio del proceso es %f" % statistics.mean(tiempoV))
print("La desviacion estandar es %f" % statistics.stdev(tiempoV))
print("\n")