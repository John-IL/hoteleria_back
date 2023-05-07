CREATE PROCEDURE update_client(
            IN _table json)
            
BEGIN
	DECLARE error_msg TEXT DEFAULT '';
	DECLARE error_code INT;
  	DECLARE EXIT HANDLER FOR SQLEXCEPTION 
  	
  	BEGIN
      GET DIAGNOSTICS CONDITION 1 error_msg = MESSAGE_TEXT;
      SELECT JSON_OBJECT("code",500,"message",error_msg) response;
    END;
	
  	start transaction;
	       
		if(json_length(_table) <= 0) then 
		
			select JSON_OBJECT("code",500,"message","Ingrese los datos.") response;
			rollback;
		
		else
			
 			UPDATE api_clients set first_name = _table->>'$.first_name', last_name = _table->>'$.last_name', country_id = _table->>'$.country',
 								phone = _table->>'$.phone', email = _table->>'$.email', document_type_id = _table->>'$.document_type',
 								document_number = _table->>'$.document_number', status = _table->>'$.status' where id = _table->>'$.id'; 
 							  
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","Satisfactoriamente") response;
         
  END