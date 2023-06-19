CREATE PROCEDURE get_dashboard_data()
BEGIn
	
	DECLARE _users int;
	DECLARE _rooms int;
	DECLARE _reserves int;
	DECLARE _sales int;


	SELECT count(*) into _users FROM api_userprofile u WHERE u.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH);
	
	select count(ar1.id) into _rooms from api_room ar1 where id not in (
		select ar.room_id from api_reservedatedetail ar 
		where (CURDATE() BETWEEN ar.start_date and ar.end_date)
	);
	
	SELECT count(*) into _reserves from api_reserve r WHERE r.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH);
	
	SELECT SUM(r.total)  into _sales from api_reserve r WHERE r.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH);
	
	SELECT _users, _rooms, _reserves, if(_sales is null, 0, _sales) _sales;
	
	
END