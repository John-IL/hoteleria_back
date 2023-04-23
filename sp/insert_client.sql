CREATE  PROCEDURE insert_client(
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
		
			select JSON_OBJECT("code",500,"message","data cannot be null") response;
			rollback;
		
		else
			
 			insert into api_clients  (first_name, last_name, country_id, phone, email, document_type_id, document_number,created_at, status) 
 						value (_table->>'$.first_name',_table->>'$.last_name', _table->>'$.country', _table->>'$.phone', _table->>'$.email',_table->>'$.document_type',
 								_table->>'$.document_number',now(), 1);
 							  
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","transaction successful") response;
         
  END