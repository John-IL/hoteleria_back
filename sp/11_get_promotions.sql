CREATE PROCEDURE get_promotions(
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
          COUNT(p.id) INTO cc
        FROM
          api_promotion p
        WHERE
        		CASE
            			WHEN (date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
              					THEN DATE(p.created_at) BETWEEN date_from AND date_to
            
            			WHEN(date_to IS NOT NULL OR date_to != "") 
              					THEN DATE(p.created_at) <= date_to
            
            			WHEN(date_from IS NOT NULL OR date_from != "") 
              					THEN DATE(p.created_at) >= date_from
            	ELSE TRUE END
          
          		AND 
            			IF(search_txt IS NULL, TRUE, (
              							p.name like CONCAT('%', search_txt, '%')
             				 			OR p.description LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              							)
              					)
           		
            	AND 
            				IF(_status is NULL, TRUE, p.status = _status)
           			;
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT p.name, p.image, p.description, p.cost, p.status,  ",  cc ," cc 
             FROM api_promotion p 
            WHERE ",
            
            CASE
              		WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                			THEN CONCAT(" date(p.created_at) between '", date_from, "' AND '", date_to,"' AND ")
              
             		WHEN(date_to IS NOT NULL OR date_to != "") 
                			THEN CONCAT(" date(p.created_at) <= '", date_to, "' AND ")
              
              		WHEN(date_from IS NOT NULL OR date_from != "") 
                			THEN CONCAT(" date(p.created_at) >= '", date_from, "' AND ")
           ELSE CONCAT(" true and ") END,
              
           IF(search_txt IS NULL OR search_txt = '', ' true and ', 
               CONCAT("( p.name like '%", search_txt, "%'
                        or p.description like '%", search_txt, "%') and ")),
                        
            if(_status is null, ' true ',	CONCAT(" p.status = ", _status, " ")),
              
            " order by p.created_at ", orderBy, " limit ", perpage, " offset ", npage, ";"
          
          );
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
        
    
END