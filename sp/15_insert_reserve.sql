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
		
			select JSON_OBJECT("code",500,"message","data cannot be null") response;
			rollback;
		
		else
			
 			insert into api_reserve (reserve_date,observation,total,client_id,payment_method_id,personal,created_at) 
 						value (_table->>'$.reserve_date',_table->>'$.observation',_table->>'$.total',_table->>'$.client',_table->>'$.payment_method',_table->>'$.personal',now());
 			
 			 set @insert_id = @@identity;
                        
			 while i < JSON_LENGTH(_detail) do
			    set @start_date = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].start_date')));
             	set @end_date = JSON_EXTRACT(_detail,CONCAT('$[',i,'].end_date'));
             	set @room = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].room')));
				set @cost = JSON_UNQUOTE(JSON_EXTRACT(_detail,CONCAT('$[',i,'].cost')));
			   
			   	insert into api_reservedatedetail (start_date,end_date,cost,reserve_id,room_id) value(@start_date,@end_date,@cost,@insert_id,@room);
			   	select i+1 into i;
			   	
             end while;
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","transaction successful") response;
         
  END