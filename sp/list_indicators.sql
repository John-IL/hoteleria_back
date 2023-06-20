CREATE PROCEDURE get_dashboard_data()
BEGIn
	
	DECLARE _clients int;
    DECLARE _last_clients int;
	DECLARE _rooms int;
	DECLARE _reserves int;
	DECLARE _sales decimal(10,2);
	DECLARE _last_reserves int;
	DECLARE _last_sales decimal(10,2);


	SELECT count(c.id) into _clients FROM api_clients c WHERE MONTH(c.created_at) = MONTH(CURDATE());
    SELECT count(c.id) into _last_clients FROM api_clients c WHERE MONTH(c.created_at) = (MONTH(CURDATE()) - 1);
	
	select count(ar1.id) into _rooms from api_room ar1 where id not in (
		select ar.room_id from api_reservedatedetail ar 
		where (CURDATE() BETWEEN ar.start_date and ar.end_date)
	);
	
	SELECT count(r.id) into _reserves from api_reserve r WHERE MONTH(r.created_at) = MONTH(CURDATE());
	
	SELECT SUM(r.total)  into _sales from api_reserve r WHERE MONTH(r.created_at) = MONTH(CURDATE());

	SELECT count(r.id) into _last_reserves from api_reserve r WHERE MONTH(r.created_at) = (MONTH(CURDATE())-1);
	
	SELECT SUM(r.total)  into _last_sales from api_reserve r WHERE MONTH(r.created_at) = (MONTH(CURDATE())-1);
	
	SELECT _clients,_last_clients, _rooms, _reserves,_last_reserves, if(_sales is null, 0, _sales) _sales, _last_sales;
	
	
END