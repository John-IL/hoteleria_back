CREATE PROCEDURE insert_room(
            IN _table json)
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
	       
		if(json_length(_table) <= 0) then 
		
			select JSON_OBJECT("code",500,"message","data cannot be null") response;
			rollback;
		
		else
			
 			insert into api_room  (
 			name,
 			slug,
 			guest_number,
 			number,
 			description,
 			has_bed,
 			has_tv,
 			has_hot_water,
 			has_jacuzzi,
 			has_private_bathroom,
 			has_couch,
 			has_balcony,
 			has_wifi,
 			cost,
 			status,
 			created_at,
 			category_id,
 			floor_id,
 			promotion_id)
 			value (
 			_table->>'$.name',
 			_table->>'$.slug',
 			_table->>'$.guest_number',
 				_table->>'$.number',
 			_table->>'$.description',
 			_table->>'$.has_bed',
 			_table->>'$.has_tv',
 			_table->>'$.has_hot_water',
 			_table->>'$.has_jacuzzi',
 			_table->>'$.has_private_bathroom',
 			_table->>'$.has_couch',
 			_table->>'$.has_balcony',
 			_table->>'$.has_wifi',
 			_table->>'$.cost',
 			_table->>'$.status',
 			now(),
 			_table->>'$.category',
 			_table->>'$.floor',
 			_table->>'$.promotion');
 			
		end if;
	
	commit;
	
	select JSON_OBJECT("code",200,"message","transaction successful") response;
         
  END