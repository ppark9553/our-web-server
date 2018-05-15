DROP TRIGGER IF EXISTS updated_projectstate_trigger on tracker_projectstate;
DROP FUNCTION IF EXISTS notify_projectstate();

CREATE FUNCTION notify_projectstate() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    PERFORM pg_notify('projectstate'::TEXT, NEW.id::TEXT);
    RETURN NULL;
END;
$$;

CREATE TRIGGER updated_projectstate_trigger AFTER INSERT ON tracker_projectstate
FOR EACH ROW EXECUTE PROCEDURE notify_projectstate();
