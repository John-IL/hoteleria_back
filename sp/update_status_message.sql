CREATE PROCEDURE update_status_message(
          in _id_message int
          )
BEGIN
	DECLARE error_msg TEXT DEFAULT '';
	DECLARE error_code INT;
  	DECLARE EXIT HANDLER FOR SQLEXCEPTION 
  	
  	BEGIN
      GET DIAGNOSTICS CONDITION 1 error_msg = MESSAGE_TEXT;
      SELECT JSON_OBJECT("code",500,"message",error_msg) response;
    END;
    	start transaction;
   update api_messages set was_readed = 1 where id = _id_message;
  
  commit;
 
 select JSON_OBJECT("code",200,"message","Satisfactoriamente") response;
END