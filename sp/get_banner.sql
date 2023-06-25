CREATE PROCEDURE get_banners(
          IN search_txt VARCHAR(250),
          IN perpage INT,
          IN npage INT,
          IN orderBy varchar(250),
          IN date_from DATE,
          IN date_to DATE,
          
          IN _status INT
        )
BEGIN 
        
        DECLARE cc INT DEFAULT 0;
        
        SELECT
          COUNT(*) INTO cc
        FROM
          api_banners ab 
        WHERE
        
          CASE
            WHEN (date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
              THEN DATE(ab.created_at) BETWEEN date_from AND date_to
            
            WHEN(date_to IS NOT NULL OR date_to != "") 
              THEN DATE(ab.created_at) <= date_to
            
            WHEN(date_from IS NOT NULL OR date_from != "") 
              THEN DATE(ab.created_at) >= date_from
            ELSE TRUE END
          
          AND 
          
            IF(search_txt IS NULL, TRUE, (
              ab.name like CONCAT('%', search_txt, '%')
              ))
              
            and if(_status is null, true, (
            ab.status = _status
            ))
            
            ;
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT ab.id, ab.name, ab.image, ab.status, ab.created_at, ar.number ,  ",  cc ," cc 
              from api_banners ab join api_room ar on ar.id = ab.room_id  WHERE ",
            
            CASE
              WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                THEN CONCAT(" date(ab.created_at) between '", date_from, "' AND '", date_to,"' AND ")
              
              WHEN(date_to IS NOT NULL OR date_to != "") 
                THEN CONCAT(" date(ab.created_at) <= '", date_to, "' AND ")
              
              WHEN(date_from IS NOT NULL OR date_from != "") 
                THEN CONCAT(" date(ab.created_at) >= '", date_from, "' AND ")
              
              ELSE CONCAT("true and ") END,
              
            IF(search_txt IS NULL OR search_txt = '', ' true and ', 
               CONCAT("( ab.name like '%", search_txt, "%' and ")),
                        
            IF(_status is null, ' true ', 
              CONCAT(" ab.status = ", _status ," ")
            
            ),
              
            CONCAT(" order by ab.created_at ", orderBy, " limit ", perpage, " offset ", npage, ";")
          
          );
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
        
        end