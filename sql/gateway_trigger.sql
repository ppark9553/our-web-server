DROP TRIGGER IF EXISTS updated_gatewaystate_trigger on gateway_gatewaystate;
DROP FUNCTION IF EXISTS notify_gatewaystate();

CREATE FUNCTION notify_gatewaystate() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    PERFORM pg_notify('gatewaystate'::TEXT, NEW.id::TEXT);
    RETURN NULL;
END;
$$;

CREATE TRIGGER updated_gatewaystate_trigger AFTER INSERT ON gateway_gatewaystate
FOR EACH ROW EXECUTE PROCEDURE notify_gatewaystate();
