CREATE PROCEDURE get_reserves(
          IN search_txt VARCHAR(250),
          IN perpage INT,
          IN npage INT,
          IN order_by varchar(20),
          IN desc_by varchar(4),
          IN date_from DATE,
          IN date_to DATE
        )
BEGIN 
        
        DECLARE cc INT DEFAULT 0;
        
        SELECT
          COUNT(r.id) INTO cc
        FROM
          api_reserve r
          join api_clients c on c.id = r.client_id
          join api_paymentmethods pm on pm.id = r.payment_method_id
          join api_userprofile up on up.id = r.personal_id
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
              r.observation like CONCAT('%', search_txt, '%')
              OR concat(c.first_name,' ',c.last_name) LIKE CONCAT('%', IFNULL(search_txt, ''), '%')
              ))
            ;
        
        SET
          npage = perpage *(npage -1);
        
        SET
          @query = CONCAT(
            "SELECT r.id, r.total,r.observation,pm.name method_payment,concat(up.first_name,' ',up.last_name) personal, r.status, concat(c.first_name,' ',c.last_name) client, r.reserve_date,  ",  cc ," cc 
             FROM  api_reserve r
         inner join api_clients c on c.id = r.client_id
          inner join api_paymentmethods pm on pm.id = r.payment_method_id
			inner join api_userprofile up on up.id = r.personal_id
            WHERE ",
            
            CASE
              WHEN(date_to IS NOT NULL AND date_from IS NOT NULL OR date_to != "" AND date_from != "") 
                THEN CONCAT(" date(r.created_at) between '", date_from, "' AND '", date_to,"' ")
              
              WHEN(date_to IS NOT NULL OR date_to != "") 
                THEN CONCAT(" date(r.created_at) <= '", date_to, "' ")
              
              WHEN(date_from IS NOT NULL OR date_from != "") 
                THEN CONCAT(" date(r.created_at) >= '", date_from, "' ")
              
              ELSE CONCAT(" true ") END,
              
            IF(search_txt IS NULL OR search_txt = "", " ", 
               CONCAT(" and ( r.observation like '%",search_txt,"%' 
							  or concat(c.first_name,' ',c.last_name) like '%",search_txt,"%' )"
               		  )),
                        
              
            " order by r.reserve_date ", desc_by, " limit ", perpage, " offset ", npage, ";");
        
        PREPARE state FROM  @query;
        EXECUTE state;
        DEALLOCATE PREPARE state;
        
  END