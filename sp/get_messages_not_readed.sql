CREATE PROCEDURE get_messages_not_readed()
BEGIN
	select concat(am.first_name,' ',am.last_name) full_name from api_messages am where was_readed = 0;
END