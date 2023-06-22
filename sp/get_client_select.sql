CREATE PROCEDURE get_clients_select(
)

BEGIN

	select id, concat(first_name,' ',last_name) name from api_clients where status = 1;

END