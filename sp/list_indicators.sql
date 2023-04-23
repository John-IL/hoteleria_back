CREATE PROCEDURE get_dashboard_data()
BEGIn
	
	DECLARE _users int;
	DECLARE _rooms int;
	DECLARE _reserves int;
	DECLARE _sales int;


	SELECT count(*) into _users FROM api_userprofile u WHERE u.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH);
	SELECT count(*) into _rooms from api_room r WHERE r.status = 1;
	SELECT count(*) into _reserves from api_reserve r WHERE r.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH);
	SELECT SUM(r.total)  into _sales from api_reserve r WHERE r.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH);
	
	SELECT _users, _rooms, _reserves, if(_sales is null, 0, _sales) _sales;
	
	
END