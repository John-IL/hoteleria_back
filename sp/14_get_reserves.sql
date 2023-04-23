CREATE PROCEDURE get_reserves(
          IN search_txt VARCHAR(250),
          IN perpage INT,
          IN npage INT,
          IN orderBy varchar(10),
          IN date_from DATE,
          IN date_to DATE,
          
          IN _room int)
          
BEGIN 
        DECLARE cc INT DEFAULT 0;
        
        SELECT
          COUNT(r.id) INTO cc
        FROM
          api_reserve r
          inner join api_reservedatedetail rd on rd.reserve_id = r.id
          inner join api_clients c on c.id = r.client_id
        WHERE
        		CASE
            			WHEN (date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
              					THEN DATE(rd.start_date) BETWEEN date_from AND date_to
            
            			WHEN(date_to IS NOT NULL OR date_to != "") 
              					THEN DATE(rd.start_date) <= date_to
            
            			WHEN(date_from IS NOT NULL OR date_from != "") 
              					THEN DATE(rd.start_date) >= date_from
            	ELSE TRUE END
          
          		AND 
            			IF(search_txt IS NULL, TRUE, (
              							concat(c.first_name,' ',c.last_name) like CONCAT('%', search_txt, '%')
              							OR r.observation like CONCAT('%', ifnull(search_txt, ''), '%')
              							)
              					)
              	AND
						IF(_room IS NULL, TRUE, (
								rd.room_id = _room
						));
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT r.total, r.reserve_date, r.observation, r.client, r.payment_method_id, r.personal, ",  cc ," cc ,  
			count(rd.id) ndetail, 
 JSON_ARRAYAGG(JSON_OBJECT('id',rd.id,'cost',rd.cost, 'start_date',rd.start_date,'end_date',rd.end_date,'room',rd.room_id)) detail FROM api_reserve r 
			inner join api_reservedatedetail rd on rd.reserve_id = r.id
			inner join api_clients c on c.id = r.client_id
            WHERE ",
            
            CASE
              		WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                			THEN CONCAT(" date(rd.start_date) between '", date_from, "' AND '", date_to,"' AND ")
              
             		WHEN(date_to IS NOT NULL OR date_to != "") 
                			THEN CONCAT(" date(rd.start_date) <= '", date_to, "' AND ")
              
              		WHEN(date_from IS NOT NULL OR date_from != "") 
                			THEN CONCAT(" date(rd.start_date) >= '", date_from, "' AND ")
           ELSE CONCAT(" true and ") END,
              
           IF(search_txt IS NULL OR search_txt = '', ' true ', 
               CONCAT("( concat(c.first_name,' ',c.last_name) like '%", search_txt, "%'
                        or r.observation like '%", search_txt, "%') and ")),
                        
           if(_room is null, ' true ',	CONCAT(" dt.room_id = ", _room, " ")),
                        
            " group by r.id order by r.created_at ", orderBy, " limit ", perpage, " offset ", npage, ";"
          
          );
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
        
    
END