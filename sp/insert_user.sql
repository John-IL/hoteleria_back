CREATE PROCEDURE insert_user(
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
    set @role_id = _data->>'$.role';
   
    insert into api_userprofile (first_name, last_name ,email, password, phone, country_id,
    							document_type_id, document_number, personal_type, role_id , is_active, is_staff, created_at) 
          value (_data->>'$.first_name', _data->>'$.last_name', _data->>'$.email',_data->>'$.password_user', _data->>'$.phone', _data->>'$.country',
         _data->>'$.document_type', _data->>'$.document_number', _data->>'$.personal_type',@role_id, true, false ,now());
        
     set @last_id = last_insert_id();
        
    if @role_id = 1 then
    
    	insert into api_usersections (module_section_id, user_id, created_at) 
    	select ms.id, @last_id, now() from api_modulesections ms; 
    else
    insert into api_usersections (module_section_id, user_id, created_at) 
    	select ms.id, @last_id, now() from api_modulesections ms where ms.id in (1,2,3,4); 
    
    end if;
    
          
   -- end main content
  end if;

commit;

select JSON_OBJECT("code",200,"message","Usuario registrado correctamente") response;
end