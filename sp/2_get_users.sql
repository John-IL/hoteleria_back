CREATE DEFINER=`root`@`localhost` PROCEDURE `hotel`.`get_users`(
          IN search_txt VARCHAR(250),
          IN perpage INT,
          IN npage INT,
          IN orderBy varchar(10),
          IN date_from DATE,
          IN date_to DATE ,
          
          in _active bool,
          in _country int,
          in _document_type int,
          in _role int
          )
BEGIN 
        DECLARE cc INT DEFAULT 0;
        
        SELECT
          COUNT(up.id) INTO cc
        FROM
          api_userprofile up
        WHERE
        
          CASE
            WHEN (date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
              THEN DATE(up.created_at) BETWEEN date_from AND date_to
            
            WHEN(date_to IS NOT NULL OR date_to != "") 
              THEN DATE(up.created_at) <= date_to
            
            WHEN(date_from IS NOT NULL OR date_from != "") 
              THEN DATE(up.created_at) >= date_from
            ELSE TRUE END
          
          AND 
          
            IF(search_txt IS NULL, TRUE, (
              CONCAT(up.first_name,' ',up.last_name) like CONCAT('%', search_txt, '%')
              OR up.phone LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              OR up.email LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              or up.document_number like CONCAT('%', ifnull(search_txt, ''), '%')))
             
           
            and if(_active is null, true, 
            up.is_active = _active
            )
            
            and if(_country is null,true, 
            up.country_id = _country
            )
            
            and if(_document_type is null,true,
            up.document_type_id = _document_type
            )
            
            and if(_role is null, true, 
            up.role_id = _role
            )   
           
           ;
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT up.id, concat(up.first_name,' ',up.last_name) full_name, up.phone, up.email, up.document_number, up.is_active, 
             up.created_at, r.name role, c.name country, dt.name document_type,  ",  cc ," cc 
             FROM api_userprofile up 
            inner join api_roles r on r.id = up.role_id
            inner join api_staticcountries c on c.id = up.country_id
			inner join api_staticdocumenttypes dt on dt.id = up.document_type_id
            WHERE ",
            
            CASE
              WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                THEN CONCAT(" date(up.created_at) between '", date_from, "' AND '", date_to,"' AND ")
              
              WHEN(date_to IS NOT NULL OR date_to != "") 
                THEN CONCAT(" date(up.created_at) <= '", date_to, "' AND ")
              
              WHEN(date_from IS NOT NULL OR date_from != "") 
                THEN CONCAT(" date(up.created_at) >= '", date_from, "' AND ")
              
              ELSE CONCAT(" true and ") END,
              
            IF(search_txt IS NULL OR search_txt = '', ' true and ', 
               CONCAT("( concat(up.first_name,' ',up.last_name) like '%", search_txt, "%'
                        or up.phone like '%", search_txt, "%'
                        or up.email like '%", search_txt, "%'
                        or up.document_number like '%", search_txt, "%') and ")),
                        
            IF(_active is null, ' true and ', CONCAT(" up.is_active = ", _active ," and ")),
            
            if(_country is null, ' true and ', CONCAT(" up.country_id = ", _country, " and ")),
            
            if(_document_type is null, ' true and ', CONCAT( " up.document_type_id  = ", _document_type, " and ")),
            
            if(_role is null, ' true ',	CONCAT(" up.role_id = ", _role, " ")),
              
            " order by up.created_at ", orderBy, " limit ", perpage, " offset ", npage, ";"
          
          );
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
        
    
END