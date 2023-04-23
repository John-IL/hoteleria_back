CREATE PROCEDURE get_reserves(
          IN search_txt VARCHAR(250),
          IN perpage INT,
          IN npage INT,
          IN orderBy varchar(250),
          IN date_from DATE,
          IN date_to DATE
        )
BEGIN 
        
        DECLARE cc INT DEFAULT 0;
        
        SELECT
          COUNT(t.id) INTO cc
        FROM
          api_testimonials t
          inner join api_clients c on c.id = t.client_id
          inner join api_room r on r.id = t.room_id 
        WHERE
        
          CASE
            WHEN (date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
              THEN DATE(t.created_at) BETWEEN date_from AND date_to
            
            WHEN(date_to IS NOT NULL OR date_to != "") 
              THEN DATE(t.created_at) <= date_to
            
            WHEN(date_from IS NOT NULL OR date_from != "") 
              THEN DATE(t.created_at) >= date_from
            ELSE TRUE END
          
          AND 
          
            IF(search_txt IS NULL, TRUE, (
              t.description like CONCAT('%', search_txt, '%')
              OR concat(c.first_name,' ',c.last_name) LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              OR r.number LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              ))
            ;
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT t.id, t.description, re.id reserve_id, t.status, concat(c.first_name,' ',c.last_name) client,r.number,  ",  cc ," cc 
             FROM  api_testimonials t
          inner join api_clients c on c.id = t.client_id
          inner join api_room r on r.id = t.room_id 
inner join api_reserve re on re.id = t.reserve_id 
            WHERE ",
            
            CASE
              WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                THEN CONCAT(" date(t.created_at) between '", date_from, "' AND '", date_to,"' AND ")
              
              WHEN(date_to IS NOT NULL OR date_to != "") 
                THEN CONCAT(" date(t.created_at) <= '", date_to, "' AND ")
              
              WHEN(date_from IS NOT NULL OR date_from != "") 
                THEN CONCAT(" date(t.created_at) >= '", date_from, "' AND ")
              
              ELSE CONCAT("true and ") END,
              
            IF(search_txt IS NULL OR search_txt = '', ' true ', 
               CONCAT("( concat(c.first_name,' ',c.last_name) like '%", search_txt, "%'
                        OR r.number like '%", search_txt, "%'
                        or t.description like '%", search_txt, "%' ")),
                        
              
            CONCAT(" order by t.created_at ", orderBy, " limit ", perpage, " offset ", npage, ";")
          
          );
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
        
  END