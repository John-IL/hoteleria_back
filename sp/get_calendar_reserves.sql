CREATE PROCEDURE get_calendar_reserves(
in _from date,
in _to date
)
BEGIN
	SELECT * FROM api_reservedatedetail ar where (ar.start_date BETWEEN _from and _to or ar.end_date BETWEEN _from and _to ); 

END