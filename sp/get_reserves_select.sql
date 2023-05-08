CREATE PROCEDURE get_reserves_select(
	in _client int
)
BEGIN

select re.id, JSON_ARRAYAGG(JSON_OBJECT('id',ro.id,'name',ro.name,'number',ro.`number`)) rooms from api_reserve re 
join api_reservedatedetail rd on rd.reserve_id = re.id
join api_room ro on ro.id = rd.room_id
where re.client_id = _client
group by re.id;


END