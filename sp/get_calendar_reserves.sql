CREATE PROCEDURE get_calendar_reserves(
in _from date,
in _to date
)
BEGIN
	SELECT ar.id, ar.start_date , ar.end_date, CONCAT(ac.first_name, ' ', ac.last_name) client  FROM api_reservedatedetail ar 
	left join api_room r on ar.room_id = r.id
	left join api_reserve ar2 on ar.reserve_id = ar2.id
	left join api_clients ac on ar2.client_id = ac.id 
	 where (ar.start_date BETWEEN _from and _to or ar.end_date BETWEEN _from and _to ); 

END