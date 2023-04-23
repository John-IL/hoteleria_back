CREATE PROCEDURE get_method_select(
)

BEGIN

	select ap.id , ap.name  from api_paymentmethods ap;

END