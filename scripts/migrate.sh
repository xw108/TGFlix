
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.channels (
    id integer NOT NULL,
    channel_id bigint NOT NULL
);

CREATE SEQUENCE public.channels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.channels_id_seq OWNED BY public.channels.id;

CREATE TABLE public.files (
    id integer NOT NULL,
    msg_id bigint NOT NULL,
    ch_id bigint NOT NULL,
    eps smallint DEFAULT 1,
    downs bigint DEFAULT 0 NOT NULL,
    hide boolean DEFAULT false NOT NULL,
    upd_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP,
    slug character varying NOT NULL,
    qlty character varying(20),
    movie_id bigint NOT NULL,
    ses smallint DEFAULT 1,
    size character varying(20)
);

CREATE SEQUENCE public.files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.files_id_seq OWNED BY public.files.id;

CREATE TABLE public.genre (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    slug character varying(30) NOT NULL,
    "desc" character varying,
    cover_img character varying
);

CREATE SEQUENCE public.genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.genre_id_seq OWNED BY public.genre.id;

CREATE TABLE public.images (
    id integer NOT NULL,
    ch_id bigint,
    msg_id bigint NOT NULL
);

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying NOT NULL,
    "desc" character varying,
    cover_img bigint DEFAULT 1,
    hide boolean DEFAULT false,
    genre integer[],
    slug character varying NOT NULL,
    is_series boolean DEFAULT true NOT NULL
);

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;

CREATE TABLE public.temp_data (
    id integer NOT NULL,
    c_id bigint NOT NULL,
    m_id bigint,
    ses smallint DEFAULT 0,
    slug_base character varying DEFAULT ''::character varying,
    is_series boolean DEFAULT true NOT NULL
);

CREATE SEQUENCE public.temp_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.temp_data_id_seq OWNED BY public.temp_data.id;

ALTER TABLE ONLY public.channels ALTER COLUMN id SET DEFAULT nextval('public.channels_id_seq'::regclass);

ALTER TABLE ONLY public.files ALTER COLUMN id SET DEFAULT nextval('public.files_id_seq'::regclass);

ALTER TABLE ONLY public.genre ALTER COLUMN id SET DEFAULT nextval('public.genre_id_seq'::regclass);

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);

ALTER TABLE ONLY public.temp_data ALTER COLUMN id SET DEFAULT nextval('public.temp_data_id_seq'::regclass);

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_cid_un UNIQUE (channel_id);

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_un UNIQUE (msg_id);

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_un UNIQUE (id, slug);

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_un UNIQUE (msg_id);

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.temp_data
    ADD CONSTRAINT temp_data_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.temp_data
    ADD CONSTRAINT temp_data_un UNIQUE (c_id);

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_fk FOREIGN KEY (ch_id) REFERENCES public.channels(channel_id) ON DELETE CASCADE;

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_fk_1 FOREIGN KEY (movie_id) REFERENCES public.movies(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_fk FOREIGN KEY (ch_id) REFERENCES public.channels(channel_id) ON DELETE CASCADE;

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_fk FOREIGN KEY (cover_img) REFERENCES public.images(id);

ALTER TABLE ONLY public.temp_data
    ADD CONSTRAINT temp_data_fk FOREIGN KEY (c_id) REFERENCES public.channels(channel_id) ON DELETE CASCADE;

ALTER TABLE ONLY public.temp_data
    ADD CONSTRAINT temp_data_moviesid_fk FOREIGN KEY (m_id) REFERENCES public.movies(id) ON DELETE CASCADE;

