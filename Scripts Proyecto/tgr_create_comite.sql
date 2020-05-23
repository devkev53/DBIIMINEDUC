/* Trigger 3: Para cada nuevo cliente que se registre en la BDD,
   crearle una nueva cuenta de tipo Monetario con Q100.00 de saldo, con su movimiento inicial
*/
create or replace trigger trg_create_comite
  AFTER INSERT ON ESCUELA
  for each row
declare
  codigo number;
  nombre varchar;
begin

  -- seleccionamos el codigo siguiente de la secuencia
  SELECT NEW_COMITE.NEXTVAL INTO codigo FROM Dual;

  SELECT concat('C-', :new.nombre) into nombre from Dual;

  -- creando el comite
  INSERT INTO COMITE (ID, NOMBRE, DESCRIPCION, FECHA_CREA, ESCUELA_ID)
  VALUES (codigo, 100, nombre, 'Comite para manejos de fonod', SYSDATE, :new.codigo);

end trg_nueva_cuenta;
