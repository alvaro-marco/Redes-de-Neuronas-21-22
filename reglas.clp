(defrule crearSesion ;; Esta regla inicializa la sesión, saluda y explica las reglas
  (not(object (is-a SESION) (nombreJuego ?juego) (nombreBambino ?bam))) ;; DUDA: se hace así que no haya una instancia de sesión???
  (object (is-a JUEGO)(nombre ?juego))
  (object (is-a BAMBINO)(nombre ?bam)(saludo ?salBambino)(personalidad ?pers))
  ?elOtro <- (object(is-a BAMBINO))
  (object (is-a LISTAPERSONALIDADES)(juego ?juego)(adaptadoA ?pers)(saludo ?sal)(reglas ?r))
    =>
    ;;Inicializar sesión
    (make-instance of SESION (nombreJuego ?juego)(nombreBambino ?bam)) ;; Creamos la instancia sesión para consultar en el resto de reglas
    (printout t "----- Creando sesión de " ?juego " con " ?bam crlf)
    ;;Saludo
    (printout t "¡Hola, " ?bam "! " ?sal  crlf)
    (printout t ?salBambino crlf)
    ;;Reglas
    (printout t "Te cuento las reglas:" crlf ?r crlf)
    (printout t "¡Entendido!" crlf)
    (printout t "Venga, enconces empiezo yo, así ves como se juega" crlf)
    ;;Creamos el turno, cambiamos la fase y eliminamos la instancia del otro niño
    (send ?elOtro delete)
    (make-instance of TURNO (fase tirada)(jugador robot)) ;; Creamos la instancia sesión para consultar en el resto de reglas
)


(defrule TiradaDado
  ;;Condiciones necesarias
  (object (is-a SESION) (nombreJuego ?juego) (nombreBambino ?bam)) ;; Que exista una sesión
  ?turno <- (object (is-a TURNO) (fase tirada)) ;; Que la fase de juego sea tirar dado/piedra
  ;;Instancias necesarias para la tirada
  (object (is-a DADO) (valorDado ?dado))
  =>
  (modify-instance ?turno (valorDado ?dado)(fase movimiento)) ;; Cambiamos el valor del dado escogido y la fase de juego´
  (printout t "He sacado un " ?dado crlf)
)

(defrule CambiarTurnoaBambino
  (object (is-a SESION) (nombreJuego ?juego) (nombreBambino ?bam))
  ?turno <- (object (is-a TURNO) (fase cambioTurno)(jugador robot))
  =>
  (printout t "Venga, ahora es tu turno, bambino" crlf)
  (modify-instance ?turno (jugador bambino)(fase tirada))
)
(defrule CambiarTurnoaRobot
  (object (is-a SESION) (nombreJuego ?juego) (nombreBambino ?bam))
  ?turno <- (object (is-a TURNO) (fase cambioTurno)(jugador bambino))
  =>
  (printout t "Te toca a tí, señor robot" crlf)
  (modify-instance ?turno (jugador robot)(fase tirada))
)


(defrule CasillaNormalOca
  ;;Condiciones necesarias
  (object (is-a SESION) (nombreJuego oca) (nombreBambino ?bam)) ;; Que exista una sesión
  ?turno <- (object (is-a TURNO)(valorDado ?dado)(fase movimiento)) ;; Que la fase de juego sea tirar dado/piedra
  ;;Instancias necesarias
  ?jugador <- (object(is-a JUGADOR)(posicion ?posJug))
  ?casilla <- (object(is-a CASILLA)(nombreJuego oca)(tipo normal)(posicion ?posCas))
  (test (= ?posCas (+ ?posJug ?dado)))
  =>
  (modify-instance ?jugador (posicion (+ ?posJug ?dado)));;Sumamos el avance marcado en el dado
  (modify-instance ?turno (fase cambioTurno));; Cambio de fase para que juegue el siguiente
  (printout t  "Estoy en la posicion " ?posJug ", avanzo " ?dado " casillas, hasta la posición " (+ ?posJug ?dado) crlf)
)

; ;; en esta regla se añaden tanto las casillas oca, como las puente, como la muerte (avance y retroceso)
(defrule CasillaAvanzaRetrocedeOca
  ;;Condiciones necesarias
  (object (is-a SESION) (nombreJuego oca) (nombreBambino ?bam)) ;; Que exista una sesión
  ?turno <- (object (is-a TURNO)(valorDado ?dado)(fase movimiento)) ;; Que la fase de juego sea tirar dado/piedra
  ;;Instancias necesarias
  ?jugador <- (object(is-a JUGADOR)(posicion ?posJug))
  ?casilla <- (object(is-a CASILLA)(nombreJuego oca)(tipo movextra)(posicion ?posCas) (nuevoValorDado ?sumar) (mensaje ?mensaje))
  (test (= ?posCas (+ ?posJug ?dado)))
  =>
  (modify-instance ?jugador (posicion (+ ?sumar (+ ?posJug ?dado))));;Sumamos el avance marcado en el dado
  (printout t ?mensaje crlf) 
  (modify-instance ?turno (fase cambioTurno));; Cambio de fase para que juegue el siguiente
  (printout t  "Estoy en la posicion " ?posJug ", avanzo " ?dado " casillas, hasta la posición " (+ ?posJug ?dado) crlf)
)
;PREGUNTAS
;SE PUEDE HACER NOMBRE JUEGO ?NOMJUEGO Y HACERLO PARA AMBAS, CON EL VALOR DE RONDAS SE DEBERÍA PODER CREO

; (defrule Casillafin
;   ;; Condiciones necesarias
;   ;; el numero de rondas para ganar de juego tiene que ser el mismo que el numero de rondas ganadas para el jugador
;   ;; 1 para la oca y 3 para la rayuela
;   ;; la casilla tiene que ser de tipo final
;   ;; el juego de la sesion no se define para que puedan ser ambos
;   (object (is-a SESION) (nombreJuego ?juego) (nombreBambino ?bam)) ;; Que exista una sesión
;   ?turno <- (object (is-a TURNO)(valorDado ?dado)(fase movimiento)) ;; Que la fase de juego sea tirar dado/piedra
;   ;;Instancias necesarias
;   ?juego <- (object(is-a JUEGO) (nombre ?juego) (rondas ?rondas)) 
;   ?jugador <- (object(is-a JUGADOR)(posicion ?posJug)(rondasGanadas ?rondas))
;   ?casilla <- (object(is-a CASILLA)(nombreJuego ?juego)(tipo final)(posicion ?posCas))
;    ; si es solo para la oca posicion seria 40, sino no hace falta ponerlo 
;   (test (> ?posCas (+ ?posJug (- ?dado 1)))
  
;   =>
;   ;;este primer modify instance creo que no haría falta porque ya se sabría con el test de arriba que se ha llegado al final, 
;   ;; no hace falta cambiar la posición del jugador porque no se va a utilizar despues, se termina el juego 
;   (modify-instance ?turno (fase fin));; Cambio de fase para que juegue el siguiente
;   (printout t  "Avanzo " ?dado " casillas, hasta la posición " (+ ?posJug ?dado) crlf)
;   (printout t "¡¡Fin del juego!! se ha llegado a la casilla final")
;   (halt)
; )
  
  
  

; (defrule CasillaEspera
;   ;;Condiciones necesarias
;   (object (is-a SESION) (nombreJuego oca) (nombreBambino ?bam)) ;; Que exista una sesión
;   ?turno <- (object (is-a TURNO)(valorDado ?dado)(fase movimiento)) ;; Que la fase de juego sea tirar dado/piedra
;   ;;Instancias necesarias
;   ?jugador <- (object(is-a JUGADOR)(posicion ?posJug))
;   ?casilla <- (object(is-a CASILLA)(nombreJuego oca)(tipo espera)(posicion ?posCas))
;   (test (= ?posCas (+ ?posJug ?dado)))
;   =>
;   (modify-instance ?jugador (posicion (+ ?posJug ?dado)));;Sumamos el avance marcado en el dado
;   ;; (modify-instance ?jugador2 (numTurnos (+ ?nT 1))) habria que cambiar el numero de turnos del jugador que no ha caido en la carcel
;   (printout t "Pierdes un turno, has caido en la carcel" crlf) 
;   (modify-instance ?turno (fase cambioTurno));; Cambio de fase para que juegue el siguiente
; )

;;Reglas de la Rayuela
;; preguntas
;; el jugador salta y completara una ronda si se cumplen las siguientes condiciones:
; el jugador no se cae 
; el jugador no pisa una línea
; el jugador salta la casilla en la que está la piedra
; el jugador llega al final y cambia de dirección
; el jugador recoge la piedra
; el jugador llega otra vez a la casilla de inicio 
; rondas ganadas += 1

;;DILEMAS
;; se obtiene el valor del dado
;; se salta de uno en uno?
;; como se avanza 
;; como se retrocede














;; Inspiración y formato BORRAR---------------------------------------------------------------------------------
  ; (defrule r-ACTIVIDAD-2
  ; (object (is-a A-2-ENTRADA) (entrada ?e) (salida ?sal) (recurso ?r) (entrada-2 ?e2) (duracion ?d))
  ; (object (is-a RECURSO) (nombre ?r) (estado on))
  ; ?pr1<- (object (is-a PRODUCTO) (nombre ?e))
  ; ?pr2<- (object (is-a PRODUCTO) (nombre ?e2))
  ; ?dur <- (tiempo ?t)
  ; =>
  ; (retract ?dur)
  ; (assert (tiempo (+ ?t ?d)))
  ; (unmake-instance ?pr1 ?pr2)
  ; (make-instance of PRODUCTO-ELABORADO (nombre ?sal))
  ; (printout t "Los productos " ?e ", " ?e2 " se transforman en " ?sal crlf)
  ; (printout t "El proceso lleva " (+ ?t ?d) " horas" crlf))