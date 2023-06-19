CREATE PROCEDURE get_available_rooms(in _start_date date, in _end_date date)
BEGIN
	
	select re.*,(re.price * re.reserves_day) sub_total, _start_date start_date, _end_date end_date,  ((re.price * re.reserves_day) - re.discount) total from(
	    SELECT ro.id, ro.number, ro.cost price, ap.cost discount, ap.id code, ap.name promotion,
	    ro.guest_number, ro.has_hot_water, ro.has_jacuzzi, ro.has_balcony, ro.has_wifi,
	    if(DATEDIFF(_end_date, _start_date) < 1 ,1, DATEDIFF(_end_date,_start_date)) reserves_day 
		FROM api_room ro
		JOIN api_promotion ap on ap.id = ro.promotion_id
		LEFT JOIN api_reservedatedetail dt ON dt.room_id = ro.id
    		AND ( dt.start_date BETWEEN _start_date AND _end_date
    		OR dt.end_date BETWEEN _start_date AND _end_date)
			WHERE dt.room_id IS NULL
	) as re;
   
END