import pygame
import random as rn
import math

# iniciar pygame		
pygame.init()

# crear la pantalla
pantalla = pygame.display.set_mode( ( 800 , 600 ) ) 
	
# título e ícono
pygame.display.set_caption( "Naves" )
icono = pygame.image.load( "planeta.png" )
pygame.display.set_icon( icono )

# fondo de pantalla
fondo = pygame.image.load( "espacio.jpg" )
	
# variables del jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0
jugador_y_cambio = 0

# variables del enemigo
img_enemigo = pygame.image.load( "ufo.png" )
enemigo_x = rn.randint( 0 , 736 )
enemigo_y = 50
enemigo_x_cambio = rn.choice( ( 0.1 , -0.1  ) )
enemigo_y_cambio = 0

# variables de la bala
img_bala = pygame.image.load( "bala.png" )
bala_x = 0
bala_y = 0
bala_y_cambio = 1
bala_visible = False
	
# colocar al jugador
def jugador( x , y ):
	pantalla.blit( img_jugador , ( x, y ) )

# colocar al enemigo
def enemigo( x , y ):
	pantalla.blit( img_enemigo , ( x , y ) )

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
	enemigo_x += enemigo_x_cambio

	# modificar ubicaión bala
	if bala_y < -6:
		bala_visible = False
	if bala_visible:
		disparar( bala_x , bala_y )
		bala_y -= bala_y_cambio

	#colision con bala
	colision = detectar_colision( enemigo_x , enemigo_y , bala_x , bala_y )
	if colision == True:
		bala_y == jugador_y
		bala_visible = False

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

	# limitaciones en el movimiento del enemigo
	if enemigo_x <= 0:
		enemigo_x_cambio = 0.1
	elif enemigo_x >= 736:
		enemigo_x_cambio = -0.1
			
	enemigo( enemigo_x , enemigo_y )
	jugador( jugador_x , jugador_y )

	# actualizar
	pygame.display.update()


