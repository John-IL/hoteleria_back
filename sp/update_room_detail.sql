CREATE PROCEDURE sp_update_room_detail(
            IN _table json,
            IN _detail json,
            IN _detail_deleted varchar(250))
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
		
			select JSON_OBJECT("code",500,"message","Ingrese los datos.") response;
			rollback;
		
		else
			
 			update api_roomcategory set name = _table->>'$.name', slug = _table->>'$.slug', color = _table->>'$.color', image = _table->>'$.image', description = _table->>'$.description'
 				where id = _table->>'$.id';
 			
 			delete from api_roomcategorydetail where FIND_IN_SET(id, _detail_deleted);
 			
			 while i < JSON_LENGTH(_detail) do
			 	
			    set @description = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].description')));
             	set @icon = JSON_EXTRACT(_detail,CONCAT('$[',i,'].icon'));
             
			   	insert into api_roomcategorydetail (room_category_id,description,icon,created_at) value(_table->>'$.id',@description,@icon,now());
			   
			   	select i+1 into i;
			   	
             end while;
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","Satisfactoriamente") response;
         
  END