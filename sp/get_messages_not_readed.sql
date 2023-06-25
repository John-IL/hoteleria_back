CREATE PROCEDURE get_messages_not_readed()
BEGIN
	select * from api_messages am where was_readed = 0;
END