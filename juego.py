import pygame
import random as rn
import math

# iniciar pygame		
pygame.init()

# crear la pantalla
pantalla = pygame.display.set_mode( ( 800 , 600 ) ) 
	
# título e ícono
pygame.display.set_caption( "Naves" )
icono = pygame.image.load( "c:/Users/user/Desktop/Projects/first_game/images/planeta.png" )
pygame.display.set_icon( icono )

# fondo de pantalla
fondo = pygame.image.load( "c:/Users/user/Desktop/Projects/first_game/images/espacio.jpg" )
	
# variables del jugador
img_jugador = pygame.image.load( "c:/Users/user/Desktop/Projects/first_game/images/astronave.png" )
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0
jugador_y_cambio = 0
colisiones = 0
terminado = False

# variables del enemigo en listas
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 24

for i in range( cantidad_enemigos ):
	img_enemigo.append( pygame.image.load( "c:/Users/user/Desktop/Projects/first_game/images/ufo.png" ) )
	enemigo_x.append(  rn.randint( 0 , 736 ) )
	enemigo_y.append( rn.randint( 0 , 250 ) )
	enemigo_x_cambio.append( rn.choice( ( 0.5 , -0.5 ) ) )
	enemigo_y_cambio.append( rn.randint( 10 , 40 ) )

# variables de la bala
img_bala = pygame.image.load( "c:/Users/user/Desktop/Projects/first_game/images/bala.png" )
bala_x = 0
bala_y = 0
bala_y_cambio = 3
bala_visible = False

# puntaje
puntaje = 0
fuente = pygame.font.Font( "freesansbold.ttf" , 32 )
texto_x = 10
texto_y = 10

# texto final del juego
fuente_final = pygame.font.Font( "freesansbold.ttf" , 50 )

def texto_final():
	mi_fuente_final = fuente_final.render( "Fin del juego" , True , ( 255 , 255 , 255 )  )
	pantalla.blit( mi_fuente_final , ( 220 , 200 ) )
	
# colocar al jugador
def jugador( x , y ):
	pantalla.blit( img_jugador , ( x, y ) )

# colocar al enemigo
def enemigo( x , y , i ):
	pantalla.blit( img_enemigo[ i ] , ( x , y ) )


# función disparar bala
def disparar( x , y ):
	global bala_visible
	bala_visible = True
	pantalla.blit( img_bala , ( x , y - 16 ) )

#Función detectar colisiones:
def detectar_colision( x1 , y1 , x2 , y2 ):
	distancia = math.sqrt( ( x2 - x1 )**2 + ( y2 - y1 )**2 )
	if distancia < 30:
		return True
	else:
		return False

# función mostrar puntaje
def mostrar_puntaje( x , y ):
	texto = fuente.render( f"Puntaje: { puntaje }" , True , ( 255 , 255 , 255 ) )
	pantalla.blit( texto , ( x , y ) )

# agregar música
pygame.mixer.music.load( "c:/Users/user/Desktop/Projects/first_game/music/universe.mp3" )
pygame.mixer.music.set_volume( 0.5 )
pygame.mixer.music.play( -1 )


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
				if terminado == False:
					sonido_bala = pygame.mixer.Sound( "c:/Users/user/Desktop/Projects/first_game/music/laser.mp3" )
					sonido_bala.play()
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
		enemigo_x[ i ] += enemigo_x_cambio[ i ]

		# fin del juego por llegada
		if enemigo_y[ i ] > 600:
			for k in range( cantidad_enemigos ):
				enemigo_y[ k ] = 1000
			jugador_y = -1000
			terminado = True
			texto_final()
			break

		# fin del juego por choque con la nave
		colision_naves = False
		colision_naves = detectar_colision( jugador_x , jugador_y , enemigo_x[ i ] , enemigo_y[ i ] )
		if colision_naves == True:
			for k in range( cantidad_enemigos ):
				enemigo_y[ k ] = 1000
			sonido_explosion_nave = pygame.mixer.Sound( "c:/Users/user/Desktop/Projects/first_game/music/explosion_nave.mp3" )
			sonido_explosion_nave.play()
			jugador_y = -1000
			terminado = True
			texto_final()
			break
						
		# limitaciones en el movimiento del enemigo
		if enemigo_x[ i ] <= 0:
			enemigo_x_cambio[ i ] = 0.5
			enemigo_y[ i ] += enemigo_y_cambio[ i ]
		elif enemigo_x[ i ] >= 736:
			enemigo_x_cambio[ i ] = -0.5
			enemigo_y[ i ] += enemigo_y_cambio[ i ]
				
		enemigo( enemigo_x[ i ] , enemigo_y[ i ] , i )

	# modificar ubicaión bala
	if bala_y < -6:
		bala_visible = False
	if bala_visible:
		disparar( bala_x , bala_y )
		bala_y -= bala_y_cambio

	#colision con bala
	colision = False
	for i in range( cantidad_enemigos ):
		colision = detectar_colision( enemigo_x[ i ] , enemigo_y[ i ] , bala_x , bala_y )

		if colision == True:
			bala_y = jugador_y
			bala_visible = False
			sonido_explosion = pygame.mixer.Sound( "c:/Users/user/Desktop/Projects/first_game/music/explosion.mp3" )
			sonido_explosion.play()
			enemigo_x[ i ] = rn.randint( 0 , 736 ) 
			enemigo_y[ i ] = rn.randint( 0 , 250 )
			enemigo_x_cambio[ i ] = rn.choice( ( 0.5 , -0.5 ) ) 
			enemigo_y_cambio[ i ] = rn.randint( 25 , 60 ) 
			puntaje += 1  

	# jugador atravesando pantalla en x
	if jugador_x <= -33:
		jugador_x = 833
	elif jugador_x >= 833:
		jugador_x = -33
	
	# jugador limitando pantalla en y
	if jugador_y <= 0 and jugador_y >= -128:
		jugador_y = 0
	elif jugador_y >= 568 and jugador_y <=700:
		jugador_y = 568


	jugador( jugador_x , jugador_y )

	mostrar_puntaje( texto_x , texto_y )

	# actualizar
	pygame.display.update()
