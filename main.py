import random
import statistics
# Menu del resturante
Menu = {
    60 : 'pizza-hawaina',
    45 : 'pizza-peperoni',
    55 : 'pizza-mexicana',
    45 : 'pizza-4-quesos',
    50 : 'pizza-champiñon',
    50 : 'pizza-margarita',
    40 : 'pizza-con-jamon',
    65 : 'pizza-vegetariana',
    50 : 'pizza-italiana',
    55 : 'pizza-carnivora'}
#%%
# Agente 
## Reglas del cocinero
ReglasCocinero = {'espera':'rayar-queso',
                    'llevar-pedido-al-cocinero':'recibir-pedido',
                    'recibir-pedido':'preparar-masa',
                    'preparar-masa':'preparar-salsa',
                    'preparar-salsa':'preparar-ingredientes',
                    'preparar-ingredientes':'hornear-pizza',
                    'hornear-pizza':'comida-lista',
                    'comida-lista':'espera'}
Calificaciones = {'pizza-hawaina': 4,
                'pizza-peperoni': 5,
                'pizza-mexicana': 5,
                'pizza-4-quesos': 6,
                'pizza-champiñon': 6,
                'pizza-margarita': 7,
                'pizza-con-jamon': 5,
                'pizza-vegetariana': 8,
                'pizza-italiana': 5,
                'pizza-carnivora': 9}

class AgenteCocinero:
    def __init__(self,reglas,calificaciones):
        self.reglas = reglas
        self.calificaciones = calificaciones
    
    def actuar(self, percepcion):
        if not percepcion:
            return "espera"
        if percepcion in self.reglas.keys():
            return self.reglas[percepcion]
        else:
            return self.reglas["espera"]
    
    def cocinar(self, puntuacion_media):
        preparar_masa=random.randint(puntuacion_media-2,puntuacion_media+2)
        preparar_salsa=random.randint(puntuacion_media-2,puntuacion_media+2)
        preparar_ingredientes=random.randint(puntuacion_media-2,puntuacion_media+2)
        pizza=[preparar_masa,preparar_salsa,preparar_ingredientes]
        return statistics.mean(pizza)
#%%
# Agente Basado en Modelo
## Reglas del mesero
ReglasMesero = {'espera':'limpiar',
                'comensal-entra':'saludar',
                'mesa-encontrada':'llevar-al-comensal',
                'esperar-comensal':'dar-menu',
                'comensal-con-menu':'preparar-lapiz',
                'comensal-pregunta':'dar-recomendacion',
                'esperar-pedido':'preparar-cuaderno',
                'pedido-anotado':'llevar-pedido-al-cocinero',
                'entregar-pedido':'esperar-plato',
                'comida-lista':'llevar-comida',
                'comensal-paga':'limpiar-mesa'}
## modelo de comportamiento del mesero
ModeloMesero = {('espera','limpiar','entrar-al-restaurante'):'comensal-entra',
                ('comensal-entra','saludar','esperar-al-mesero'):'mesa-encontrada',
                ('mesa-encontrada','llevar-al-comensal','ir-a-la-mesa'):'esperar-comensal',
                ('esperar-comensal','dar-menu','mirar-menu'):'comensal-con-menu',
                ('comensal-con-menu','preparar-lapiz','pedir-recomendacion'):'comensal-pregunta',
                ('comensal-pregunta','dar-recomendacion','revisar-presupuesto'):'esperar-pedido',
                ('esperar-pedido','preparar-cuaderno','pedir-plato'):'pedido-anotado',
                ('pedido-anotado','llevar-pedido-al-cocinero','esperar-plato'):'entregar-pedido',
                ('entregar-pedido','esperar-plato','esperar-plato2'):'comida-lista',
                ('comida-lista','llevar-comida','recibir-plato'):'espera',
                ('espera','limpiar','puntuar'):'comensal-paga',
                ('comensal-paga','limpiar-mesa','pagar'):'espera',}

class AgenteMesero:
    def __init__(self,menu, modelo, reglas, estado_inicial, accion_inicial):
        self.menu = menu
        self.modelo = modelo
        self.reglas = reglas
        self.estado_inicial = estado_inicial
        self.accion_inicial = accion_inicial
        self.accion = None
        self.estado = self.estado_inicial
        self.ult_accion = self.accion_inicial
    
    def actuar(self, percepcion):
        if not percepcion:
            return self.accion_inicial
        clave = (self.estado, self.ult_accion, percepcion)
        if clave not in self.modelo.keys():
            self.accion = None
            self.estado = self.estado_inicial
            self.ult_accion = self.accion_inicial
            return self.accion_inicial
        self.estado = self.modelo[clave]
        accion = self.reglas[self.estado]
        self.ult_accion = accion
        return accion

# Agente Reactivo simple
## reglas del comensal o posibles estados lineales
ReglasComensal = {'entrar-al-restaurante':'esperar-al-mesero',
        'esperar-al-mesero':'ir-a-la-mesa',
        'ir-a-la-mesa':'mirar-menu',
        'mirar-menu':'pedir-recomendacion',
        'pedir-recomendacion':'revisar-presupuesto',
        'revisar-presupuesto':'pedir-plato',
        'pedir-plato':'esperar-plato',
        'esperar-plato':'esperar-plato2',
        'esperar-plato2':'recibir-plato',
        'recibir-plato': 'comer',
        'comer':'puntuar',
        'puntuar': 'pagar',
        'pagar':'salir'}

def listas(media,esfuerzo, inicio):
        lista=[]
        for i in range(esfuerzo):
            lista.append(random.randint(inicio,media))
        return lista

class AgenteComensal:
    def __init__(self, reglas, presupuesto):
        self.reglas = reglas
        self.presupuesto = presupuesto

    def actuar(self, percepcion): ## falta implementar mejor
        if not percepcion:
            return "esperar"
        if percepcion in self.reglas.keys():
            return self.reglas[percepcion]
    
    def elegir_plato(self, menu, recomendacion):
        precio_platos = list(menu.keys())
        tamaño = len(precio_platos)
        candidatos=[]
        for i in range(tamaño):
            if precio_platos[i] <= self.presupuesto:
                candidatos.append(menu[precio_platos[i]])
        if recomendacion in candidatos:
            if random.randint(0,2) >= 1:
                return recomendacion
            else:
                return random.choice(candidatos)
        else:
            return random.choice(candidatos)

    def puntuar_plato(self, puntuacion_media, esfuerzo_del_chef):
        if puntuacion_media > esfuerzo_del_chef:
            puntuaciones = listas(puntuacion_media,esfuerzo_del_chef, inicio=0)
            puntuacion = statistics.mean(puntuaciones)
            return puntuacion
        elif puntuacion_media==esfuerzo_del_chef:
            puntuaciones = listas(puntuacion_media+1,esfuerzo_del_chef,inicio=puntuacion_media-1)
            puntuacion = statistics.mean(puntuaciones)
            return puntuacion
        else:
            puntuaciones = listas(esfuerzo_del_chef, esfuerzo_del_chef, inicio=puntuacion_media)
            puntuacion = statistics.mean(puntuaciones)
            return puntuacion

# hacer una funcion para mejorar los ciclos fors
presupuesto=random.randint(40,70)
comensal = AgenteComensal(ReglasComensal, presupuesto)
mesero = AgenteMesero(Menu,ModeloMesero,ReglasMesero,"espera","limpiar")
chefsito = AgenteCocinero(ReglasCocinero,Calificaciones)
accion_comensal_base = 'entrar-al-restaurante'
accion_mesero_base = 'entrar-al-restaurante'
accion_chef = 'espera'

def ciclofor(i):
    global accion_mesero_base
    global accion_comensal_base
    global accion_chef
    for j in range(i):
        print(f'mesero: {accion_mesero_base}')
        print(f'comensal: {accion_comensal_base}')
        print(f'chef: {accion_chef}')
        accion_mesero_base = mesero.actuar(accion_comensal_base)
        accion_comensal_base = comensal.actuar(accion_comensal_base)
        accion_chef = chefsito.actuar(accion_mesero_base)
        while accion_chef != "rayar-queso": #imprime antes de tiempo REVISAR
            accion_chef = chefsito.actuar(accion_chef)
            print(f'chef: {accion_chef}')

ciclofor(7)
Recomendacion=random.choice(list(Menu))
plato = comensal.elegir_plato(Menu,Menu[Recomendacion])
print(f'*******comensal pidio {plato}, el mesero recomendo: {Menu[Recomendacion]}*******')
print(f'*******presupuesto del comensal: {presupuesto}*******')

ciclofor(5)
puntuacion_plato = comensal.puntuar_plato(random.randint(0,10),int(chefsito.cocinar(Calificaciones[plato]))) #enviar puntuacion media
print(f'*******puntuacion de {plato}:{puntuacion_plato}')

ciclofor(2)
print(f'mesero: {accion_mesero_base}')
print(f'comensal: {accion_comensal_base}')
