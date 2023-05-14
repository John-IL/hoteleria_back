CREATE PROCEDURE insert_category(
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
			set @url_image = concat(MD5(rand()),'.jpg');
 			insert into api_roomcategory  (name,slug,color,image,status,created_at,description) 
 						value (_table->>'$.name',_table->>'$.slug',_table->>'$.color',@url_image,_table->>'$.status',now(), _table->>'$.description');
 							  
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","Satisfactoriamente",'image',@url_image) response;
         
  END