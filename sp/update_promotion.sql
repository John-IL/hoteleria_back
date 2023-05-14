CREATE PROCEDURE update_promotion(
            IN _table json)
BEGIN
	DECLARE error_msg TEXT DEFAULT '';
	DECLARE error_code INT;
    DECLARE original_image text DEFAULT '';
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
		 set @url_image = concat(MD5(rand()),'.jpg');
		 select image into original_image from api_roomcategory where id = _table->>'$.id';
			
 			update api_promotion set name = _table->>'$.name', 
 			image = if(_table->>'$.image' = 0 ,@url_image,_table->>'$.image'),
 			description = _table->>'$.description', 
 			cost = _table->>'$.cost', 
 			status = _table->>'$.status'
 			where id = _table->>'$.id';
 							  
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","Satisfactoriamente","old",original_image, "new",@url_image) response;
         
  END