create or replace FUNCTION VALIDAR_PAGO_ACTIVIDAD 
(
  ID_ACTIVIDAD NUMBER, MONTO NUMBER 
) RETURN NUMBER AS 
  -- Creamos las variables a utilizar
    CodigoSeq INTEGER;
    id_plan NUMBER;
    id_comite NUMBER;
    Ciclo NUMBER;
    Fondo NUMBER;
    saldo_fondo NUMBER;
    monto_pago NUMBER;
    ERROR_SINISALDO EXCEPTION;
    Result INTEGER;

-- Inicio de la funcion
BEGIN
  -- Obtenemos el MONTO
  monto_pago := MONTO;
  
  -- Tomamos la planificacion de ACTIVIDAD
  select PLAINFICACION_ID into id_plan from ACTIVIDAD
    where ID=ID_ACTIVIDAD;
  
  -- Tomamos el valor de comite de PLANIFICACION
  select COMITE_ID into id_comite from PLANIFICACION
    where ID=id_plan;
  
  -- Tomamos el valor del ciclo de PLANIFICACION
  select CICLO into Ciclo from PLANIFICACION
    where ID=id_plan;
  
  -- Tomamos el valor de la actividad
  select ID into Fondo from FONDO
    where COMITE_ID=id_comite and CICLO=Ciclo;

-- Tomamos el valor de la actividad
  select SALDO into saldo_fondo from FONDO
    where COMITE_ID=id_comite and CICLO=Ciclo;
    
  -- Se guarda el siguiente valor secuencian en CodigoSeq
    SELECT SEQ_BITACORAFONDOS.NextVal
        INTO CodigoSeq From Dual;
  
  -- Se inserta un nuevo registro en la tabla BitacoraFondos
    INSERT INTO BITACORAFONDOS (CODIGO, DESCRIPCION, FECHA, CODIGO_FONDO)
        VALUES (CodigoSeq, 
            'PAGO DE ACTIVIDAD DEL CICLO || Ciclo',
            SYSDATE, Fondo);

    /* Se crea el marcador para regresar al roolback */
    SAVEPOINT RegistroPAGO;
  
  -- obtenemos solo el año de la fecha del sistema
  SELECT EXTRACT(YEAR FROM sysdate) INTO Ciclo FROM dual;
  
  -- Validamos si existe con un If
  IF (monto_pago > saldo_fondo) THEN
    -- Si existe una asignacion lanzamos la exepcion
        RAISE ERROR_SINISALDO;
    END IF;
  
  -- Se cumplio todo actualizamos la bitacora
    UPDATE BITACORAFONDOS
    SET ESTADO = 'OK' WHERE CODIGO = CodigoSeq;
  
  -- Confirmar transaccion
    COMMIT;
    DBMS_OUTPUT.put_line('Se ha generado un pago del fondo: || Fondo');
    Result := 0;
  
  RETURN NULL;
  
  EXCEPTION
  WHEN ERROR_SINISALDO THEN
    DBMS_OUTPUT.put_line('No se cuenta con Saldo suficiente en el FONDO');
    ROLLBACK TO SAVEPOINT RegistroAsignacion;
    UPDATE BITACORAFONDOS SET ESTADO = 'ERROR'
    WHERE CODIGO = CodigoSeq;
    return 1;
    COMMIT;
    
  WHEN OTHERS THEN
     DBMS_OUTPUT.put_line
        ('Error en la transaccion: ' || SQLERRM);
     DBMS_OUTPUT.put_line('Se deshacen las modificaciones.');
     ROLLBACK;
END VALIDAR_PAGO_ACTIVIDAD;