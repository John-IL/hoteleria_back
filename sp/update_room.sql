CREATE PROCEDURE update_room(
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
			
 			update api_room  set name = _table->>'$.name', slug  = _table->>'$.slug', 
 			guest_number  = _table->>'$.guest_number', `number`  = _table->>'$.number', 
 			description  = _table->>'$.description', has_bed  = _table->>'$.has_bed',
 			has_tv  = _table->>'$.has_tv', has_hot_water  = _table->>'$.has_hot_water',
 			 has_jacuzzi  = _table->>'$.has_jacuzzi', has_private_bathroom  = _table->>'$.has_private_bathroom',
 			  has_couch  = _table->>'$.has_couch', has_balcony  = _table->>'$.has_balcony',
 			   has_wifi  = _table->>'$.has_wifi', status  = _table->>'$.status',
 			    cost  = _table->>'$.cost', promotion_id  = _table->>'$.promotion_id',
 			    category_id  = _table->>'$.category_id',floor_id  = _table->>'$.floor_id'
 			where id = _table->>'$.id';
 							  
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","Satisfactoriamente") response;
         
  end