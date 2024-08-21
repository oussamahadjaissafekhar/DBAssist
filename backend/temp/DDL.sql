--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

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

--
-- Name: hypopg; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS hypopg WITH SCHEMA public;


--
-- Name: EXTENSION hypopg; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION hypopg IS 'Hypothetical indexes for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    c_custkey integer NOT NULL,
    c_name character varying(25) NOT NULL,
    c_address character varying(40) NOT NULL,
    c_city character(10) NOT NULL,
    c_nation character(15) NOT NULL,
    c_region character(15) NOT NULL,
    c_phone character(15) NOT NULL,
    c_mktsegment character(10) NOT NULL,
    supp character(1)
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- Name: dates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dates (
    d_datekey integer NOT NULL,
    d_date character(18) NOT NULL,
    d_dayofweek character(15) NOT NULL,
    d_month character(9) NOT NULL,
    d_year integer NOT NULL,
    d_yearmonthnum integer NOT NULL,
    d_yearmonth character(7) NOT NULL,
    d_daynuminweek integer NOT NULL,
    d_daynuminmonth integer NOT NULL,
    d_daynuminyear integer NOT NULL,
    d_monthnuminyear integer NOT NULL,
    d_weeknuminyear integer NOT NULL,
    d_sellingseason character(12) NOT NULL,
    d_lastdayinweekfl boolean NOT NULL,
    d_lastdayinmonthfl boolean NOT NULL,
    d_holidayfl boolean NOT NULL,
    d_weekdayfl boolean NOT NULL,
    supp character(1)
);


ALTER TABLE public.dates OWNER TO postgres;

--
-- Name: lineorder; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lineorder (
    lo_orderkey integer,
    lo_linenumber integer,
    lo_custkey integer,
    lo_partkey integer,
    lo_suppkey integer,
    lo_orderdate integer,
    lo_orderpriority character(15),
    lo_shippriority character(1),
    lo_quantity integer,
    lo_extendedprice integer,
    lo_ordtotalprice integer,
    lo_discount integer,
    lo_revenue integer,
    lo_supplycost integer,
    lo_tax integer,
    lo_commitdate integer,
    lo_shipmode character(10)
);


ALTER TABLE public.lineorder OWNER TO postgres;

--
-- Name: part; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.part (
    p_partkey integer NOT NULL,
    p_name character varying(50) NOT NULL,
    p_mfgr character(25) NOT NULL,
    p_category character(10) NOT NULL,
    p_brand character(9) NOT NULL,
    p_color character varying(11) NOT NULL,
    p_type character varying(25) NOT NULL,
    p_size integer NOT NULL,
    p_container character(10) NOT NULL,
    supp character(1)
);


ALTER TABLE public.part OWNER TO postgres;

--
-- Name: supplier; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.supplier (
    s_suppkey integer NOT NULL,
    s_name character(25) NOT NULL,
    s_address character varying(40) NOT NULL,
    s_city character(10) NOT NULL,
    s_nation character(15) NOT NULL,
    s_region character(15) NOT NULL,
    s_phone character(15) NOT NULL,
    supp character(1)
);


ALTER TABLE public.supplier OWNER TO postgres;

--
-- Name: ind; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ind ON public.lineorder USING btree (lo_custkey);


--
-- PostgreSQL database dump complete
--

