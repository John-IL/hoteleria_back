CREATE PROCEDURE get_messages(
          IN search_txt VARCHAR(250),
          IN perpage INT,
          IN npage INT,
          IN orderBy varchar(10),
          IN date_from DATE,
          IN date_to DATE ,
          
          in _status int
          )
BEGIN 
        DECLARE cc INT DEFAULT 0;
        
        SELECT
          COUNT(m.id) INTO cc
        FROM
          api_messages  m
        WHERE
        		CASE
            			WHEN (date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
              					THEN DATE(m.created_at) BETWEEN date_from AND date_to
            
            			WHEN(date_to IS NOT NULL OR date_to != "") 
              					THEN DATE(m.created_at) <= date_to
            
            			WHEN(date_from IS NOT NULL OR date_from != "") 
              					THEN DATE(m.created_at) >= date_from
            	ELSE TRUE END
          
          		AND 
            			IF(search_txt IS NULL, TRUE, (
              					CONCAT(
              							m.first_name,' ',m.last_name) like CONCAT('%', search_txt, '%')
             				 			OR m.phone LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
             				 			OR m.email LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              							)
              					)
           		
           		AND 
           				IF(_status is NULL, TRUE, m.was_readed = _status)
           
            
           			;
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT m.*,  ",  cc ," cc 
             FROM api_messages  m
            WHERE ",
            
            CASE
              		WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                			THEN CONCAT(" date(m.created_at) between '", date_from, "' AND '", date_to,"' ")
              
             		WHEN(date_to IS NOT NULL OR date_to != "") 
                			THEN CONCAT(" date(m.created_at) <= '", date_to, "' ")
              
              		WHEN(date_from IS NOT NULL OR date_from != "") 
                			THEN CONCAT(" date(m.created_at) >= '", date_from, "' ")
           ELSE CONCAT(" true ") END,
            
            if(_status is null, ' ', CONCAT(" and m.was_readed = ", _status, " ")),
            
            if(search_txt is null or search_txt = '', '', 
            ( concat(" and concat(m.first_name,' ',m.last_name) like '%",search_txt,"%' 
							or m.phone like '%",search_txt,"%' 
							or m.email like '%",search_txt,"%'" ))),
              
            " order by m.created_at ", orderBy, " limit ", perpage, " offset ", npage, ";"
          
          );
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
    
END