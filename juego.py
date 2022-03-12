import pygame
import random as rn
import math

# iniciar pygame		
pygame.init()

# crear la pantalla
pantalla = pygame.display.set_mode( ( 800 , 600 ) ) 
	
# título e ícono
pygame.display.set_caption( "Naves" )
icono = pygame.image.load( "images/planeta.png" )
pygame.display.set_icon( icono )

# fondo de pantalla
fondo = pygame.image.load( "images/espacio.jpg" )
	
# variables del jugador
img_jugador = pygame.image.load("images/astronave.png")
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0
jugador_y_cambio = 0
puntaje = 0

# variables del enemigo en listas
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 24

for i in range( cantidad_enemigos ):
	img_enemigo.append( pygame.image.load( "images/ufo.png" ) )
	enemigo_x.append(  rn.randint( 0 , 736 ) )
	enemigo_y.append( rn.randint( 0 , 250 ) )
	enemigo_x_cambio.append( rn.choice( ( 0.5 , -0.5 ) ) )
	enemigo_y_cambio.append( rn.randint( 10 , 40 ) )

# variables de la bala
img_bala = pygame.image.load( "images/bala.png" )
bala_x = 0
bala_y = 0
bala_y_cambio = 2
bala_visible = False
	
# colocar al jugador
def jugador( x , y ):
	pantalla.blit( img_jugador , ( x, y ) )

# colocar al enemigo
def enemigo( x , y , i ):
	pantalla.blit( img_enemigo[i] , ( x , y ) )

# función disparar bala
def disparar( x , y ):
	global bala_visible
	bala_visible = True
	pantalla.blit( img_bala , ( x , y-16 ) )

#Función detectar colisiones:
def detectar_colision( x1 , y1 , x2 , y2 ):
	distancia = math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
	if distancia < 30:
		return True
	else:
		return False

# loop del juego
ejecucion = True
while ejecucion:
	pantalla.blit( fondo , ( 0 , 0 ))

	for evento in pygame.event.get():
		# evento cerrar
		if evento.type == pygame.QUIT:
			ejecucion = False

		# evento presionar
		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_RIGHT:
				jugador_x_cambio = 0.3

			if evento.key == pygame.K_LEFT:
				jugador_x_cambio = -0.3

			if evento.key == pygame.K_UP:
				jugador_y_cambio = -0.3

			if evento.key == pygame.K_DOWN:
				jugador_y_cambio = 0.3

			if evento.key == pygame.K_SPACE:
				if bala_visible == False:
					bala_x = jugador_x 
					bala_y = jugador_y
					disparar( bala_x , bala_y )

		# evento soltar flechas
		if evento.type == pygame.KEYUP:
			if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
				jugador_x_cambio = 0

			if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
				jugador_y_cambio = 0
		
	# modificar ubicación del jugador
	jugador_x += jugador_x_cambio
	jugador_y += jugador_y_cambio

	# modificar ubicación del enemigo
	for i in range( cantidad_enemigos ):
		enemigo_x[i] += enemigo_x_cambio[i]
		

		# limitaciones en el movimiento del enemigo
		if enemigo_x[i] <= 0:
			enemigo_x_cambio[i] = 0.5
			enemigo_y[i] += enemigo_y_cambio[i]
		elif enemigo_x[i] >= 736:
			enemigo_x_cambio[i] = -0.5
			enemigo_y[i] += enemigo_y_cambio[i]
				
		enemigo( enemigo_x[i] , enemigo_y[i] , i)

	# modificar ubicaión bala
	if bala_y < -6:
		bala_visible = False
	if bala_visible:
		disparar( bala_x , bala_y )
		bala_y -= bala_y_cambio

	#colision con bala
	for i in range( cantidad_enemigos ):
		colision = detectar_colision( enemigo_x[ i ] , enemigo_y[ i ] , bala_x , bala_y )
		if colision == True:
			bala_y == jugador_y
			bala_visible = False
			puntaje += 1  
			enemigo_x[ i ] = rn.randint( 0 , 736 ) 
			enemigo_y[ i ] = rn.randint( 0 , 250 )
			enemigo_x_cambio[ i ] = rn.choice( ( 0.5 , -0.5 ) ) 
			enemigo_y_cambio[ i ] = rn.randint( 25 , 60 ) 

	# jugador atravesando pantalla en x
	if jugador_x <= -33:
		jugador_x = 833
	elif jugador_x > 833:
		jugador_x = -33
	
	# jugador limitando pantalla en y
	if jugador_y <= 0:
		jugador_y = 0
	elif jugador_y >= 568:
		jugador_y = 568


	jugador( jugador_x , jugador_y )

	# actualizar
	pygame.display.update()


