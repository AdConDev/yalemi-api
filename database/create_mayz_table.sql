-- Table: public.may

-- DROP TABLE IF EXISTS public.may;

CREATE TABLE IF NOT EXISTS public.may
(
    published boolean NOT NULL DEFAULT true,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    id_may integer NOT NULL DEFAULT nextval('may_id_may_seq'::regclass),
    title character varying(30) COLLATE pg_catalog."default" NOT NULL,
    content character varying(120) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT may_pkey PRIMARY KEY (id_may)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.may
    OWNER to adcon;
-- Index: ix_may_content

-- DROP INDEX IF EXISTS public.ix_may_content;

CREATE INDEX IF NOT EXISTS ix_may_content
    ON public.may USING btree
    (content COLLATE pg_catalog."default" A NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_may_title

-- DROP INDEX IF EXISTS public.ix_may_title;

CREATE INDEX IF NOT EXISTS ix_may_title
    ON public.may USING btree
    (title COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
