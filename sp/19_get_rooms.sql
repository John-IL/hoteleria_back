CREATE PROCEDURE get_rooms(
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
          COUNT(r.id) INTO cc
        FROM
          api_room r
          inner join api_roomcategory rc on rc.id = r.category_id 
          inner join api_promotion p on p.id = r.promotion_id 
          inner join api_floor f on f.id = r.floor_id
        WHERE
        
          CASE
            WHEN (date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
              THEN DATE(r.created_at) BETWEEN date_from AND date_to
            
            WHEN(date_to IS NOT NULL OR date_to != "") 
              THEN DATE(r.created_at) <= date_to
            
            WHEN(date_from IS NOT NULL OR date_from != "") 
              THEN DATE(r.created_at) >= date_from
            ELSE TRUE END
          
          AND 
          
            IF(search_txt IS NULL, TRUE, (
              r.number like CONCAT('%', search_txt, '%')
              or r.description LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              OR r.guest_number LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              OR r.name LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              ))
            ;
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT r.*,p.name promotion_name,rc.name category_name, f.number floor_number,  ",  cc ," cc 
             FROM  api_room r
          inner join api_roomcategory rc on rc.id = r.category_id 
          inner join api_promotion p on p.id = r.promotion_id 
          inner join api_floor f on f.id = r.floor_id
            WHERE ",
            
            CASE
              WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                THEN CONCAT(" date(r.created_at) between '", date_from, "' AND '", date_to,"' AND ")
              
              WHEN(date_to IS NOT NULL OR date_to != "") 
                THEN CONCAT(" date(r.created_at) <= '", date_to, "' AND ")
              
              WHEN(date_from IS NOT NULL OR date_from != "") 
                THEN CONCAT(" date(r.created_at) >= '", date_from, "' AND ")
              
              ELSE CONCAT("true and ") END,
              
            IF(search_txt IS NULL OR search_txt = '', ' true ', 
               CONCAT("( r.guest_number like '%", search_txt, "%'
                        OR r.number like '%", search_txt, "%'
						OR r.name like '%", search_txt, "%'
                        or r.description like '%", search_txt, "%' ")),
                       
            CONCAT(" order by r.created_at ", orderBy, " limit ", perpage, " offset ", npage, ";")
          
          );
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
        
  END