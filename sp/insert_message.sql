CREATE PROCEDURE insert_message( IN _table json)
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
			
 			insert into api_messages (first_name, last_name, email, phone, body, was_readed, created_at ) 
 						value (_table->>'$.first_name',_table->>'$.last_name', _table->>'$.email',
 						_table->>'$.phone', _table->>'$.body', 0, now());
 							  
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","Satisfactoriamente") response;
END