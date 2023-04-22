CREATE PROCEDURE insert_room_detail(
            IN _table json,
            IN _detail json)
            
BEGIN
	DECLARE error_msg TEXT DEFAULT '';
	DECLARE error_code INT;
	DECLARE i int default 0; 
  	DECLARE EXIT HANDLER FOR SQLEXCEPTION 
  	
  	BEGIN
      GET DIAGNOSTICS CONDITION 1 error_msg = MESSAGE_TEXT;
      SELECT JSON_OBJECT("code",500,"message",error_msg) response;
    END;
	
  	start transaction;
	       
		if(json_length(_detail) <= 0) then 
		
			select JSON_OBJECT("code",500,"message","data cannot be null") response;
			rollback;
		
		else
			
 			insert into api_roomcategory (name,slug,color,image,description,created_at) 
 						value (_table->>'$.name',_table->>'$.slug',_table->>'$.color',_table->>'$.image',_table->>'$.description',now());
 			
 			 set @insert_id = @@identity;
                        
			 while i < JSON_LENGTH(_detail) do
			    set @description = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].description')));
             	set @icon = JSON_EXTRACT(_detail,CONCAT('$[',i,'].icon'));
			   
			   	insert into api_roomcategorydetail (room_category_id,description,icon,created_at) value(@insert_id,@description, @icon, now());
			   	select i+1 into i;
			   	
             end while;
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","transaction successful") response;
         
  END