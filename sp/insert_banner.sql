CREATE PROCEDURE insert_banner(
          IN _data json)
        
BEGIN
  DECLARE error_msg TEXT DEFAULT '';
  DECLARE EXIT HANDLER FOR SQLEXCEPTION 
  
  -- validation and errors
  
  BEGIN
    GET DIAGNOSTICS CONDITION 1 error_msg = MESSAGE_TEXT;
    SELECT JSON_OBJECT("code",500,"message",error_msg) response;
  END;

  start transaction;
       
  if(json_length(_data) <= 0) then 
  
    SELECT JSON_OBJECT("code",500,"message","Ingrese los datos.") response;
    rollback;
    
    -- end validation and errors
    
  else
   -- main content
   
    insert into api_banners (name, image, created_at, status) 
          value (_data->>'$.name', _data->>'$.image',now(), 1);
          
   -- end main content
  end if;

commit;

select JSON_OBJECT("code",200,"message","Satisfactoriamente") response;
END