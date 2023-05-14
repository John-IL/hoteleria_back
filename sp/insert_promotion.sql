CREATE PROCEDURE insert_promotion(
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
 			insert into api_promotion (name,image,description,cost,status,created_at) 
 						value (_table->>'$.name',@url_image,_table->>'$.description',_table->>'$.cost',_table->>'$.status',now());
 							  
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","Satisfactoriamente",'image',@url_image) response;
         
  END