CREATE PROCEDURE update_user(
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
  
    SELECT JSON_OBJECT("code",500,"message","data cannot be null") response;
    rollback;
    
    -- end validation and errors
    
  else
   -- main content
   
    update api_userprofile set email = _data->>'$.email', phone = _data->>'$.phone', 
   								country_id = _data->>'$.country', personal_type = _data->>'$.personal_type',
   								role_id = _data->>'$.role',
   								is_active = _data->>'$.status'
   								where id = _data->>'$.id';
          
   -- end main content
  end if;

commit;

select JSON_OBJECT("code",200,"message","transaction successful") response;
END