CREATE PROCEDURE insert_reserve(
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
		
			select JSON_OBJECT("code",500,"message","Ingrese los datos.") response;
			rollback;
		
		else
			
 			insert into api_reserve (reserve_date,observation,total,client_id,payment_method_id,personal_id,created_at,status) 
 						value (now(),_table->>'$.observation',_table->>'$.total',_table->>'$.client',_table->>'$.payment_method',_table->>'$.personal',now(),1);
 			
 			 set @insert_id = @@identity;
                        
			 while i < JSON_LENGTH(_detail) do
			 	set @cost = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].total')));
			    set @start_date = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].start_date')));
             	set @end_date =  JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].end_date')));
             	set @room = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].id')));
                set @discount = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].discount')));
				set @category =  JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].promotion')));
			    set @promotion =  JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].code')));

			   	insert into api_reservedatedetail (promotion_id,category,start_date,end_date,cost,reserve_id,room_id,status,discount) 
				value(@promotion,@category,@start_date,@end_date,@cost,@insert_id,@room,1, @discount);
			   	
				select i+1 into i;
			   	
             end while;
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","Satisfactoriamente") response;
         
  END