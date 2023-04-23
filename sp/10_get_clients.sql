CREATE PROCEDURE get_clients(
          IN search_txt VARCHAR(250),
          IN perpage INT,
          IN npage INT,
          IN orderBy varchar(10),
          IN date_from DATE,
          IN date_to DATE ,
          
          in _document_type int,
          in _status int,
          in _country int
          )
BEGIN 
        DECLARE cc INT DEFAULT 0;
        
        SELECT
          COUNT(c.id) INTO cc
        FROM
          api_clients c
        WHERE
        		CASE
            			WHEN (date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
              					THEN DATE(c.created_at) BETWEEN date_from AND date_to
            
            			WHEN(date_to IS NOT NULL OR date_to != "") 
              					THEN DATE(c.created_at) <= date_to
            
            			WHEN(date_from IS NOT NULL OR date_from != "") 
              					THEN DATE(c.created_at) >= date_from
            	ELSE TRUE END
          
          		AND 
            			IF(search_txt IS NULL, TRUE, (
              					CONCAT(
              							c.first_name,' ',c.last_name) like CONCAT('%', search_txt, '%')
             				 			OR c.phone LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
             				 			OR c.email LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              							OR c.document_number like CONCAT('%', ifnull(search_txt, ''), '%')
              							)
              					)
           		
           		AND 
           				IF(_document_type is NULL, TRUE, c.document_type_id = _document_type)
            
            	AND 
            			IF(_status is NULL, TRUE, c.status = _status)
            
            	AND 
            			IF(_country is NULL, TRUE, c.country_id = _country)
            
           			;
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT c.id, c.first_name, c.last_name, c.phone, c.email, c.document_number, c.status, 
             c.created_at, co.id country, co.name country_name, dt.id document_type, dt.name document_type_name,  ",  cc ," cc 
             FROM api_clients c 
            inner join api_staticcountries co on co.id = c.country_id
			inner join api_staticdocumenttypes dt on dt.id = c.document_type_id
            WHERE ",
            
            CASE
              		WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                			THEN CONCAT(" date(c.created_at) between '", date_from, "' AND '", date_to,"' AND ")
              
             		WHEN(date_to IS NOT NULL OR date_to != "") 
                			THEN CONCAT(" date(c.created_at) <= '", date_to, "' AND ")
              
              		WHEN(date_from IS NOT NULL OR date_from != "") 
                			THEN CONCAT(" date(c.created_at) >= '", date_from, "' AND ")
           ELSE CONCAT(" true and ") END,
              
           IF(search_txt IS NULL OR search_txt = '', ' true and ', 
               CONCAT("( concat(c.first_name,' ',c.last_name) like '%", search_txt, "%'
                        or c.phone like '%", search_txt, "%'
                        or c.email like '%", search_txt, "%'
                        or c.document_number like '%", search_txt, "%') and ")),
                        
            IF(_document_type is null, ' true and ', CONCAT(" c.document_type_id = ", _document_type ," and ")),
            
            if(_status is null, ' true and ', CONCAT(" c.status = ", _status, " and ")),
            
            if(_country is null, ' true and ', CONCAT( " c.country_id  = ", _country, " ")),
            
              
            " order by c.created_at ", orderBy, " limit ", perpage, " offset ", npage, ";"
          
          );
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
    
END