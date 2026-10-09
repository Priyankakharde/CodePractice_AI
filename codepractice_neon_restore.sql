-- 
-- PostgreSQL database dump 
--

\restrict yM3qzlejMg4gN7qa8a1azEaf5x8J4UPt4X0DHIWQqpUWXybOFlIFBRdOonTCwMO

-- Dumped from database version 17.8
-- Dumped by pg_dump version 17.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bookmarks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookmarks (
    id integer NOT NULL,
    user_id integer NOT NULL,
    lesson_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    topic_name character varying(255)
);


ALTER TABLE public.bookmarks;

--
-- Name: bookmarks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bookmarks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bookmarks_id_seq;

--
-- Name: bookmarks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bookmarks_id_seq OWNED BY public.bookmarks.id;


--
-- Name: lesson_notes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lesson_notes (
    id integer NOT NULL,
    user_id integer,
    lesson_id integer,
    note_text text DEFAULT ''::text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.lesson_notes;

--
-- Name: lesson_notes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lesson_notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lesson_notes_id_seq;

--
-- Name: lesson_notes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lesson_notes_id_seq OWNED BY public.lesson_notes.id;


--
-- Name: lessons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lessons (
    id integer NOT NULL,
    subject character varying(20) NOT NULL,
    title character varying(150) NOT NULL,
    description text,
    lesson_order integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.lessons;

--
-- Name: lessons_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lessons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lessons_id_seq;

--
-- Name: lessons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lessons_id_seq OWNED BY public.lessons.id;


--
-- Name: practice_submissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.practice_submissions (
    id integer NOT NULL,
    user_id integer,
    lesson_id integer,
    code text NOT NULL,
    status character varying(30),
    execution_time double precision,
    submitted_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.practice_submissions;

--
-- Name: practice_submissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.practice_submissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.practice_submissions_id_seq;

--
-- Name: practice_submissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.practice_submissions_id_seq OWNED BY public.practice_submissions.id;


--
-- Name: progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.progress (
    id integer NOT NULL,
    user_id integer,
    lesson_id integer,
    completed boolean DEFAULT false,
    attempts integer DEFAULT 0,
    last_attempted timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.progress;

--
-- Name: progress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.progress_id_seq;

--
-- Name: progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.progress_id_seq OWNED BY public.progress.id;


--
-- Name: query_challenge_attempts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.query_challenge_attempts (
    id integer NOT NULL,
    user_id integer,
    lesson_id integer,
    query_text text,
    status character varying(30),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.query_challenge_attempts;

--
-- Name: query_challenge_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.query_challenge_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.query_challenge_attempts_id_seq;

--
-- Name: query_challenge_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.query_challenge_attempts_id_seq OWNED BY public.query_challenge_attempts.id;


--
-- Name: query_challenges; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.query_challenges (
    id integer NOT NULL,
    lesson_id integer NOT NULL,
    topic_name character varying(255) NOT NULL,
    challenge_task text NOT NULL,
    challenge_hint text,
    expected_query text NOT NULL,
    points integer DEFAULT 10,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    task text,
    hint text
);


ALTER TABLE public.query_challenges;

--
-- Name: query_challenges_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.query_challenges_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.query_challenges_id_seq;

--
-- Name: query_challenges_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.query_challenges_id_seq OWNED BY public.query_challenges.id;


--
-- Name: sql_practice_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sql_practice_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    lesson_id integer NOT NULL,
    topic_name character varying(255) NOT NULL,
    query_text text NOT NULL,
    success boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.sql_practice_history;

--
-- Name: sql_practice_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sql_practice_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sql_practice_history_id_seq;

--
-- Name: sql_practice_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sql_practice_history_id_seq OWNED BY public.sql_practice_history.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    password_hash text
);


ALTER TABLE public.users;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: bookmarks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookmarks ALTER COLUMN id SET DEFAULT nextval('public.bookmarks_id_seq'::regclass);


--
-- Name: lesson_notes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lesson_notes ALTER COLUMN id SET DEFAULT nextval('public.lesson_notes_id_seq'::regclass);


--
-- Name: lessons id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lessons ALTER COLUMN id SET DEFAULT nextval('public.lessons_id_seq'::regclass);


--
-- Name: practice_submissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.practice_submissions ALTER COLUMN id SET DEFAULT nextval('public.practice_submissions_id_seq'::regclass);


--
-- Name: progress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progress ALTER COLUMN id SET DEFAULT nextval('public.progress_id_seq'::regclass);


--
-- Name: query_challenge_attempts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_challenge_attempts ALTER COLUMN id SET DEFAULT nextval('public.query_challenge_attempts_id_seq'::regclass);


--
-- Name: query_challenges id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_challenges ALTER COLUMN id SET DEFAULT nextval('public.query_challenges_id_seq'::regclass);


--
-- Name: sql_practice_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_practice_history ALTER COLUMN id SET DEFAULT nextval('public.sql_practice_history_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: bookmarks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookmarks (id, user_id, lesson_id, created_at, topic_name) FROM stdin;
3	71	1	2026-10-03 13:44:50.964424	Variables
6	71	98	2026-10-06 11:16:14.853147	Database & Tables
7	71	100	2026-10-06 11:17:06.034124	SELECT
8	71	101	2026-10-06 11:17:17.726372	WHERE
\.


--
-- Data for Name: lesson_notes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lesson_notes (id, user_id, lesson_id, note_text, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: lessons; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lessons (id, subject, title, description, lesson_order, created_at) FROM stdin;
1	Python	Variables	Python Basics → Variables	1	2026-09-29 11:33:22.121381
2	Python	Data Types	Python Basics → Data Types	2	2026-09-29 11:33:22.121381
3	Python	Input / Output	Python Basics → Input / Output	3	2026-09-29 11:33:22.121381
4	Python	Arithmetic Operators	Operators → Arithmetic Operators	4	2026-09-29 11:33:22.121381
5	Python	Assignment Operators	Operators → Assignment Operators	5	2026-09-29 11:33:22.121381
6	Python	Comparison Operators	Operators → Comparison Operators	6	2026-09-29 11:33:22.121381
7	Python	Logical Operators	Operators → Logical Operators	7	2026-09-29 11:33:22.121381
8	Python	if / elif / else	Control Statements → if / elif / else	8	2026-09-29 11:33:22.121381
9	Python	for Loop	Control Statements → for Loop	9	2026-09-29 11:33:22.121381
10	Python	while Loop	Control Statements → while Loop	10	2026-09-29 11:33:22.121381
11	Python	Lists	Data Structures → Lists	11	2026-09-29 11:33:22.121381
12	Python	Tuples	Data Structures → Tuples	12	2026-09-29 11:33:22.121381
13	Python	Dictionaries	Data Structures → Dictionaries	13	2026-09-29 11:33:22.121381
14	Python	Sets	Data Structures → Sets	14	2026-09-29 11:33:22.121381
15	Python	Define Function	Functions → Define Function	15	2026-09-29 11:33:22.121381
16	Python	Arguments	Functions → Arguments	16	2026-09-29 11:33:22.121381
17	Python	Return Value	Functions → Return Value	17	2026-09-29 11:33:22.121381
18	Python	Lambda	Functions → Lambda	18	2026-09-29 11:33:22.121381
19	Python	Import Modules	Modules & Libraries → Import Modules	19	2026-09-29 11:33:22.121381
20	Python	Built-in Modules	Modules & Libraries → Built-in Modules	20	2026-09-29 11:33:22.121381
21	Python	External Libraries	Modules & Libraries → External Libraries	21	2026-09-29 11:33:22.121381
22	Python	Read File	File Handling → Read File	22	2026-09-29 11:33:22.121381
23	Python	Write File	File Handling → Write File	23	2026-09-29 11:33:22.121381
24	Python	Open / Close File	File Handling → Open / Close File	24	2026-09-29 11:33:22.121381
25	Python	try	Exception Handling → try	25	2026-09-29 11:33:22.121381
26	Python	except	Exception Handling → except	26	2026-09-29 11:33:22.121381
27	Python	finally	Exception Handling → finally	27	2026-09-29 11:33:22.121381
28	Python	Basic Syntax	List Comprehension → Basic Syntax	28	2026-09-29 11:33:22.121381
29	Python	With Condition	List Comprehension → With Condition	29	2026-09-29 11:33:22.121381
30	Python	Class	OOP Basics → Class	30	2026-09-29 11:33:22.121381
31	Python	Object	OOP Basics → Object	31	2026-09-29 11:33:22.121381
32	Python	Inheritance	OOP Basics → Inheritance	32	2026-09-29 11:33:22.121381
33	Python	len()	Built-in Functions → len()	33	2026-09-29 11:33:22.121381
34	Python	type()	Built-in Functions → type()	34	2026-09-29 11:33:22.121381
35	Python	range()	Built-in Functions → range()	35	2026-09-29 11:33:22.121381
36	Python	int()	Built-in Functions → int()	36	2026-09-29 11:33:22.121381
37	Python	float()	Built-in Functions → float()	37	2026-09-29 11:33:22.121381
38	Python	str()	Built-in Functions → str()	38	2026-09-29 11:33:22.121381
39	Python	sum()	Built-in Functions → sum()	39	2026-09-29 11:33:22.121381
40	Python	min()	Built-in Functions → min()	40	2026-09-29 11:33:22.121381
41	Python	max()	Built-in Functions → max()	41	2026-09-29 11:33:22.121381
42	Python	Arrays	NumPy → Arrays	42	2026-09-29 11:33:22.121381
43	Python	Indexing	NumPy → Indexing	43	2026-09-29 11:33:22.121381
44	Python	Array Operations	NumPy → Array Operations	44	2026-09-29 11:33:22.121381
45	Python	Series	Pandas → Series	45	2026-09-29 11:33:22.121381
46	Python	DataFrame	Pandas → DataFrame	46	2026-09-29 11:33:22.121381
47	Python	Read CSV	Pandas → Read CSV	47	2026-09-29 11:33:22.121381
48	Python	Select Data	Pandas → Select Data	48	2026-09-29 11:33:22.121381
49	Python	Filter Data	Pandas → Filter Data	49	2026-09-29 11:33:22.121381
50	Python	Missing Values	Data Cleaning → Missing Values	50	2026-09-29 11:33:22.121381
51	Python	Duplicates	Data Cleaning → Duplicates	51	2026-09-29 11:33:22.121381
52	Python	Data Transformation	Data Cleaning → Data Transformation	52	2026-09-29 11:33:22.121381
53	Python	Mean	Data Analysis → Mean	53	2026-09-29 11:33:22.121381
54	Python	Median	Data Analysis → Median	54	2026-09-29 11:33:22.121381
55	Python	Mode	Data Analysis → Mode	55	2026-09-29 11:33:22.121381
56	Python	describe()	Data Analysis → describe()	56	2026-09-29 11:33:22.121381
57	Python	groupby()	Data Analysis → groupby()	57	2026-09-29 11:33:22.121381
58	Python	Line Chart	Data Visualization → Line Chart	58	2026-09-29 11:33:22.121381
59	Python	Bar Chart	Data Visualization → Bar Chart	59	2026-09-29 11:33:22.121381
60	Python	Histogram	Data Visualization → Histogram	60	2026-09-29 11:33:22.121381
61	Python	Scatter Plot	Data Visualization → Scatter Plot	61	2026-09-29 11:33:22.121381
62	Python	Features	ML Basics → Features	62	2026-09-29 11:33:22.121381
63	Python	Target	ML Basics → Target	63	2026-09-29 11:33:22.121381
64	Python	Model	ML Basics → Model	64	2026-09-29 11:33:22.121381
65	Python	Prediction	ML Basics → Prediction	65	2026-09-29 11:33:22.121381
66	Python	Supervised Learning	Types of ML → Supervised Learning	66	2026-09-29 11:33:22.121381
67	Python	Unsupervised Learning	Types of ML → Unsupervised Learning	67	2026-09-29 11:33:22.121381
68	Python	Reinforcement Learning — basic idea	Types of ML → Reinforcement Learning — basic idea	68	2026-09-29 11:33:22.121381
69	Python	Regression	Supervised Learning → Regression	69	2026-09-29 11:33:22.121381
70	Python	Classification	Supervised Learning → Classification	70	2026-09-29 11:33:22.121381
71	Python	Clustering	Unsupervised Learning → Clustering	71	2026-09-29 11:33:22.121381
72	Python	K-Means — basic idea	Unsupervised Learning → K-Means — basic idea	72	2026-09-29 11:33:22.121381
73	Python	Features & Target	Dataset Preparation → Features & Target	73	2026-09-29 11:33:22.121381
74	Python	Train / Test Split	Dataset Preparation → Train / Test Split	74	2026-09-29 11:33:22.121381
75	Python	Preprocessing	Dataset Preparation → Preprocessing	75	2026-09-29 11:33:22.121381
76	Python	Scaling	Dataset Preparation → Scaling	76	2026-09-29 11:33:22.121381
77	Python	Create Model	Model Training → Create Model	77	2026-09-29 11:33:22.121381
78	Python	fit()	Model Training → fit()	78	2026-09-29 11:33:22.121381
79	Python	Training Data	Model Training → Training Data	79	2026-09-29 11:33:22.121381
80	Python	Accuracy	Evaluation → Accuracy	80	2026-09-29 11:33:22.121381
81	Python	Precision	Evaluation → Precision	81	2026-09-29 11:33:22.121381
82	Python	Recall	Evaluation → Recall	82	2026-09-29 11:33:22.121381
83	Python	MAE	Evaluation → MAE	83	2026-09-29 11:33:22.121381
84	Python	MSE	Evaluation → MSE	84	2026-09-29 11:33:22.121381
85	Python	R²	Evaluation → R²	85	2026-09-29 11:33:22.121381
86	Python	Overfitting	Overfitting & Underfitting → Overfitting	86	2026-09-29 11:33:22.121381
87	Python	Underfitting	Overfitting & Underfitting → Underfitting	87	2026-09-29 11:33:22.121381
88	Python	Import Model	Scikit-learn Basics → Import Model	88	2026-09-29 11:33:22.121381
89	Python	predict()	Scikit-learn Basics → predict()	91	2026-09-29 11:33:22.121381
90	Python	Collect Data	ML Workflow → Collect Data	92	2026-09-29 11:33:22.121381
91	Python	Clean Data	ML Workflow → Clean Data	93	2026-09-29 11:33:22.121381
92	Python	Explore Data	ML Workflow → Explore Data	94	2026-09-29 11:33:22.121381
93	Python	Prepare Data	ML Workflow → Prepare Data	95	2026-09-29 11:33:22.121381
94	Python	Train Model	ML Workflow → Train Model	96	2026-09-29 11:33:22.121381
95	Python	Evaluate Model	ML Workflow → Evaluate Model	97	2026-09-29 11:33:22.121381
96	Python	Predict	ML Workflow → Predict	98	2026-09-29 11:33:22.121381
121	Python	Python Basics	Python lesson: Python Basics	99	2026-10-03 13:43:50.846829
97	PostgreSQL	Introduction	PostgreSQL is a relational database system used to store and query structured data.	1	2026-09-29 11:33:22.121381
98	PostgreSQL	Database & Tables	A database contains tables. A table stores records in rows and attributes in columns.	2	2026-09-29 11:33:22.121381
99	PostgreSQL	Data Types	Data types tell PostgreSQL what kind of value a column can store.	3	2026-09-29 11:33:22.121381
100	PostgreSQL	SELECT	SELECT is used to read data from a table.	4	2026-09-29 11:33:22.121381
101	PostgreSQL	WHERE	WHERE filters rows that match a condition.	5	2026-09-29 11:33:22.121381
102	PostgreSQL	Operators	SQL operators are used for calculations, comparisons and logical conditions.	6	2026-09-29 11:33:22.121381
103	PostgreSQL	ORDER BY	ORDER BY sorts query results.	7	2026-09-29 11:33:22.121381
104	PostgreSQL	LIMIT	LIMIT controls how many rows PostgreSQL returns.	8	2026-09-29 11:33:22.121381
105	PostgreSQL	INSERT	INSERT adds new rows to a table.	9	2026-09-29 11:33:22.121381
106	PostgreSQL	UPDATE	UPDATE changes existing rows.	10	2026-09-29 11:33:22.121381
107	PostgreSQL	DELETE	DELETE removes rows from a table.	11	2026-09-29 11:33:22.121381
108	PostgreSQL	Aggregate Functions	Aggregate functions calculate a result from multiple rows.	12	2026-09-29 11:33:22.121381
109	PostgreSQL	GROUP BY	GROUP BY creates groups so aggregate functions can be calculated for each group.	13	2026-09-29 11:33:22.121381
110	PostgreSQL	HAVING	HAVING filters groups after GROUP BY.	14	2026-09-29 11:33:22.121381
111	PostgreSQL	JOIN	JOIN combines related data from multiple tables.	15	2026-09-29 11:33:22.121381
112	PostgreSQL	Subqueries	A subquery is a query inside another query.	16	2026-09-29 11:33:22.121381
113	PostgreSQL	CASE	CASE creates conditional values inside a SQL query.	17	2026-09-29 11:33:22.121381
114	PostgreSQL	NULL Handling	NULL represents a missing or unknown value.	18	2026-09-29 11:33:22.121381
115	PostgreSQL	Date & Time	PostgreSQL provides DATE and TIMESTAMP types and functions for time-based data.	19	2026-09-29 11:33:22.121381
116	PostgreSQL	String Functions	String functions clean and transform text values.	20	2026-09-29 11:33:22.121381
117	PostgreSQL	CTE	A Common Table Expression (CTE) creates a temporary named result for a query.	21	2026-09-29 11:33:22.121381
118	PostgreSQL	Window Functions	Window functions calculate values across related rows without collapsing them.	22	2026-09-29 11:33:22.121381
119	PostgreSQL	Data Cleaning	SQL can clean, filter and transform raw database data before analysis.	23	2026-09-29 11:33:22.121381
120	PostgreSQL	Preparing Data for ML	SQL can create a final feature table that Python or an ML pipeline can load.	24	2026-09-29 11:33:22.121381
\.


--
-- Data for Name: practice_submissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.practice_submissions (id, user_id, lesson_id, code, status, execution_time, submitted_at) FROM stdin;
\.


--
-- Data for Name: progress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.progress (id, user_id, lesson_id, completed, attempts, last_attempted) FROM stdin;
11	71	53	f	0	2026-10-08 12:34:17.10334
12	71	54	f	0	2026-10-08 12:34:18.508334
4	71	121	t	1	2026-10-08 20:31:26.410428
3	71	97	t	3	2026-10-08 20:31:38.705874
16	71	98	t	1	2026-10-08 20:31:44.572534
17	71	99	t	1	2026-10-08 20:31:48.871672
2	71	1	t	3	2026-10-08 20:32:05.600547
1	71	2	t	2	2026-10-08 20:32:09.971831
9	71	3	t	1	2026-10-08 20:32:13.440174
5	71	4	t	1	2026-10-08 20:32:21.673443
6	71	5	t	1	2026-10-08 20:32:24.805104
7	71	6	t	1	2026-10-08 20:32:28.247369
8	71	7	t	1	2026-10-08 20:32:33.438037
10	71	8	t	1	2026-10-08 20:32:52.6761
13	71	9	t	1	2026-10-08 20:32:57.690824
14	71	10	t	1	2026-10-08 20:33:02.542644
15	71	11	t	1	2026-10-08 20:33:10.136383
18	71	12	t	1	2026-10-08 20:33:14.168779
19	71	13	t	1	2026-10-08 20:33:19.14121
20	71	14	t	1	2026-10-08 20:33:24.847041
21	71	15	t	1	2026-10-08 20:33:33.44333
22	71	16	t	1	2026-10-08 20:33:36.853661
23	71	17	t	1	2026-10-08 20:33:40.961522
24	71	18	t	1	2026-10-08 20:34:14.551034
25	71	19	t	1	2026-10-08 20:34:22.428
26	71	20	t	1	2026-10-08 20:34:25.847861
27	71	21	t	1	2026-10-08 20:34:29.828682
28	71	22	f	0	2026-10-08 20:34:36.054131
29	71	23	t	1	2026-10-08 20:34:41.351556
30	71	24	t	1	2026-10-08 20:34:45.772126
31	71	25	t	1	2026-10-08 20:34:53.582224
32	71	26	t	1	2026-10-08 20:34:58.239136
33	71	27	t	1	2026-10-08 20:35:02.584431
34	71	28	t	1	2026-10-08 20:35:12.830865
35	71	29	t	1	2026-10-08 20:35:17.378701
36	71	30	t	1	2026-10-08 20:35:25.32775
37	71	31	t	1	2026-10-08 20:35:29.33081
38	71	32	t	1	2026-10-08 20:35:32.893706
39	71	33	t	1	2026-10-08 20:35:39.545595
40	71	34	t	1	2026-10-08 20:35:42.965961
41	71	35	t	1	2026-10-08 20:35:47.186396
42	71	36	t	1	2026-10-08 20:35:49.964878
43	71	37	t	1	2026-10-08 20:35:54.026139
44	71	38	t	1	2026-10-08 20:35:57.360267
45	71	39	t	1	2026-10-08 20:36:01.454409
46	71	40	t	1	2026-10-08 20:36:06.067283
\.


--
-- Data for Name: query_challenge_attempts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.query_challenge_attempts (id, user_id, lesson_id, query_text, status, created_at) FROM stdin;
\.


--
-- Data for Name: query_challenges; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.query_challenges (id, lesson_id, topic_name, challenge_task, challenge_hint, expected_query, points, created_at, task, hint) FROM stdin;
6	102	Operators	Write a query that displays students whose score is between 70 and 90.	Try using BETWEEN with the score column.	SELECT name, score\nFROM students\nWHERE score >= 70\n  AND score < 90;	10	2026-10-06 10:53:13.716615	\N	\N
7	103	ORDER BY	Write a query that displays students ordered from highest score to lowest score.	Use ORDER BY score DESC.	SELECT name, score\nFROM students\nORDER BY score DESC;	10	2026-10-06 10:53:13.716615	\N	\N
8	104	LIMIT	Write a query that displays only the first 5 rows from the students table.	Add LIMIT 5 to the query.	SELECT *\nFROM students\nLIMIT 5;	10	2026-10-06 10:53:13.716615	\N	\N
9	105	INSERT	Write a query that adds a new student named Priyanka with a score of 90.	Use INSERT INTO students.	INSERT INTO students (name, score)\nVALUES ('Priyanka', 90);	10	2026-10-06 10:53:13.716615	\N	\N
1	97	Introduction	Write a SQL query that displays the message 'Hello PostgreSQL'.	Use SELECT with a text value.	SELECT 'Hello PostgreSQL' AS message;	10	2026-10-06 10:53:13.716615	\N	\N
2	98	Database & Tables	Write a CREATE TABLE query for a students table with id, name and score columns.	Use CREATE TABLE and define the columns.	CREATE TABLE students (\n    id SERIAL PRIMARY KEY,\n    name VARCHAR(100),\n    score INTEGER\n);	10	2026-10-06 10:53:13.716615	\N	\N
3	99	Data Types	Write a SELECT query that displays an age, score, subject and active status.	Use SELECT and aliases such as age, score, subject and active.	SELECT\n    27 AS age,\n    99.5 AS score,\n    'Python' AS subject,\n    TRUE AS active;	10	2026-10-06 10:53:13.716615	\N	\N
4	100	SELECT	Write a query that selects name and score from the students table.	Use SELECT name, score FROM students.	SELECT name, score\nFROM students;	10	2026-10-06 10:53:13.716615	\N	\N
5	101	WHERE	Write a query that displays students whose score is greater than or equal to 70.	Use WHERE score >= 70.	SELECT name, score\nFROM students\nWHERE score >= 70;	10	2026-10-06 10:53:13.716615	\N	\N
10	106	UPDATE	Write a query that changes Priyanka's score to 95.	Use UPDATE, SET and WHERE.	UPDATE students\nSET score = 95\nWHERE name = 'Priyanka';	10	2026-10-06 10:53:13.716615	\N	\N
11	107	DELETE	Write a query that removes students whose score is below 30.	Use DELETE FROM with a WHERE condition.	DELETE FROM students\nWHERE score < 30;	10	2026-10-06 10:53:13.716615	\N	\N
12	108	Aggregate Functions	Write a query that calculates the number of students, average score and highest score.	Try COUNT(), AVG() and MAX().	SELECT\n    COUNT(*) AS total_students,\n    AVG(score) AS average_score,\n    MAX(score) AS highest_score\nFROM students;	10	2026-10-06 10:53:13.716615	\N	\N
13	109	GROUP BY	Write a query that calculates the average score for each department.	Use AVG(score) together with GROUP BY.	SELECT department, AVG(score) AS avg_score\nFROM students\nGROUP BY department;	10	2026-10-06 10:53:13.716615	\N	\N
14	110	HAVING	Write a query that displays departments whose average score is at least 70.	Use GROUP BY followed by HAVING.	SELECT department, AVG(score) AS avg_score\nFROM students\nGROUP BY department\nHAVING AVG(score) >= 70;	10	2026-10-06 10:53:13.716615	\N	\N
15	111	JOIN	Write a query that combines students and courses and displays the student name and course name.	Use JOIN with the related key columns.	SELECT s.name, c.course_name\nFROM students s\nJOIN courses c\n  ON s.course_id = c.id;	10	2026-10-06 10:53:13.716615	\N	\N
16	112	Subqueries	Write a query that finds students whose score is greater than the average score.	Use SELECT AVG(score) as a subquery.	SELECT name, score\nFROM students\nWHERE score > (\n    SELECT AVG(score)\n    FROM students\n);	10	2026-10-06 10:53:13.716615	\N	\N
17	113	CASE	Write a query that classifies students as High, Medium or Low based on their score.	Use CASE WHEN ... THEN ... ELSE ... END.	SELECT name, score,\nCASE\n    WHEN score >= 80 THEN 'High'\n    WHEN score >= 50 THEN 'Medium'\n    ELSE 'Low'\nEND AS level\nFROM students;	10	2026-10-06 10:53:13.716615	\N	\N
18	114	NULL Handling	Write a query that replaces NULL scores with 0.	Try COALESCE(score, 0).	SELECT name,\n       COALESCE(score, 0) AS score\nFROM students;	10	2026-10-06 10:53:13.716615	\N	\N
19	115	Date & Time	Write a query that displays the current date and current timestamp.	Use CURRENT_DATE and CURRENT_TIMESTAMP.	SELECT CURRENT_DATE AS today,\n       CURRENT_TIMESTAMP AS current_time;	10	2026-10-06 10:53:13.716615	\N	\N
20	116	String Functions	Write a query that converts a name to lowercase and calculates its length.	Try LOWER() and LENGTH().	SELECT\n    LOWER('Machine Learning') AS lower_text,\n    LENGTH('Python') AS text_length;	10	2026-10-06 10:53:13.716615	\N	\N
21	117	CTE	Write a CTE that selects students whose score is 80 or higher.	Start with WITH and create a temporary result.	WITH high_scores AS (\n    SELECT *\n    FROM students\n    WHERE score >= 80\n)\nSELECT *\nFROM high_scores;	10	2026-10-06 10:53:13.716615	\N	\N
22	118	Window Functions	Write a query that ranks students from highest score to lowest score.	Try RANK() OVER (ORDER BY score DESC).	SELECT name, score,\n       RANK() OVER (ORDER BY score DESC) AS rank\nFROM students;	10	2026-10-06 10:53:13.716615	\N	\N
23	119	Data Cleaning	Write a query that cleans student names by removing extra spaces and converting them to lowercase.	Try TRIM() and LOWER().	SELECT DISTINCT\n    TRIM(LOWER(name)) AS clean_name\nFROM students\nWHERE name IS NOT NULL;	10	2026-10-06 10:53:13.716615	\N	\N
24	120	Preparing Data for ML	Write a query that prepares clean features and a target value for machine learning.	Use SELECT, COALESCE() and CASE to create clean features.	SELECT\n    age,\n    income,\n    COALESCE(score, 0) AS score,\n    CASE\n        WHEN score >= 70 THEN 1\n        ELSE 0\n    END AS target\nFROM students;	10	2026-10-06 10:53:13.716615	\N	\N
25	97	Introduction	Write a SQL query that displays the message 'Hello PostgreSQL'.	Use SELECT with a text value.	SELECT 'Hello PostgreSQL' AS message;	10	2026-10-06 11:25:03.247504	\N	\N
\.


--
-- Data for Name: sql_practice_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sql_practice_history (id, user_id, lesson_id, topic_name, query_text, success, created_at) FROM stdin;
1	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:08:38.109342
2	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:08:41.966762
3	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:08:45.335314
4	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:08:58.548282
5	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:09:04.768016
6	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:09:19.934797
7	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:14:38.755948
8	71	97	Introduction		f	2026-10-06 10:14:43.146725
9	71	97	Introduction		f	2026-10-06 10:14:46.245911
10	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:14:52.177637
11	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:17:42.88164
12	71	98	Database & Tables	CREATE TABLE students (\n    id SERIAL PRIMARY KEY,\n    name VARCHAR(100),\n    score INTEGER\n);	t	2026-10-06 10:17:56.948399
13	71	97	Introduction	SELECT 'Hello PostgreSQL' AS message;	t	2026-10-06 10:30:36.697682
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, created_at, updated_at, password_hash) FROM stdin;
66	Piku Kharde	pikukharde@gmail.com	2026-10-02 14:53:04.002203	2026-10-02 14:53:04.002203	8d87f9ea2e01e4cd5b9ac662c0becc98:6e4b4ce35904b9d31e95289dbf7b3764d6d7ca086db529b72d9993e8af4414d7
69	Rohit Kharde	rohitkharde@gmail.com	2026-10-03 12:14:58.457062	2026-10-03 12:14:58.457062	6a792558f46338b370a588a3aea6e57b$66c1eb734ef2fa150b0a59d66967896d59ec1bf2ba5de62416a41f731dd63cae
70	Rakesh Kharde	rakeshkharde@gamil.com	2026-10-03 12:15:45.64981	2026-10-03 12:15:45.64981	d09d414f6f033e168d462eb0110a06ac$24fb75174bdb0ebfbb56801400f7cc632843c85e7dd50d8217cc7f441cc8c033
71	Priyanka Kharde	priyanka@codepractice.local	2026-10-03 13:42:51.62401	2026-10-03 13:42:51.62401	\N
\.


--
-- Name: bookmarks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookmarks_id_seq', 8, true);


--
-- Name: lesson_notes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.lesson_notes_id_seq', 1, true);


--
-- Name: lessons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.lessons_id_seq', 121, true);


--
-- Name: practice_submissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.practice_submissions_id_seq', 1, false);


--
-- Name: progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.progress_id_seq', 46, true);


--
-- Name: query_challenge_attempts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.query_challenge_attempts_id_seq', 1, false);


--
-- Name: query_challenges_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.query_challenges_id_seq', 26, true);


--
-- Name: sql_practice_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sql_practice_history_id_seq', 13, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 80, true);


--
-- Name: bookmarks bookmarks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT bookmarks_pkey PRIMARY KEY (id);


--
-- Name: bookmarks bookmarks_user_id_lesson_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT bookmarks_user_id_lesson_id_key UNIQUE (user_id, lesson_id);


--
-- Name: lesson_notes lesson_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lesson_notes
    ADD CONSTRAINT lesson_notes_pkey PRIMARY KEY (id);


--
-- Name: lessons lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_pkey PRIMARY KEY (id);


--
-- Name: practice_submissions practice_submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.practice_submissions
    ADD CONSTRAINT practice_submissions_pkey PRIMARY KEY (id);


--
-- Name: progress progress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progress
    ADD CONSTRAINT progress_pkey PRIMARY KEY (id);


--
-- Name: query_challenge_attempts query_challenge_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_challenge_attempts
    ADD CONSTRAINT query_challenge_attempts_pkey PRIMARY KEY (id);


--
-- Name: query_challenges query_challenges_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_challenges
    ADD CONSTRAINT query_challenges_pkey PRIMARY KEY (id);


--
-- Name: sql_practice_history sql_practice_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_practice_history
    ADD CONSTRAINT sql_practice_history_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: idx_bookmarks_user_lesson; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_bookmarks_user_lesson ON public.bookmarks USING btree (user_id, lesson_id);


--
-- Name: bookmarks bookmarks_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT bookmarks_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: bookmarks bookmarks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT bookmarks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: lesson_notes lesson_notes_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lesson_notes
    ADD CONSTRAINT lesson_notes_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: lesson_notes lesson_notes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lesson_notes
    ADD CONSTRAINT lesson_notes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: practice_submissions practice_submissions_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.practice_submissions
    ADD CONSTRAINT practice_submissions_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: practice_submissions practice_submissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.practice_submissions
    ADD CONSTRAINT practice_submissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: progress progress_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progress
    ADD CONSTRAINT progress_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: progress progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progress
    ADD CONSTRAINT progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: query_challenge_attempts query_challenge_attempts_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_challenge_attempts
    ADD CONSTRAINT query_challenge_attempts_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: query_challenge_attempts query_challenge_attempts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_challenge_attempts
    ADD CONSTRAINT query_challenge_attempts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: query_challenges query_challenges_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_challenges
    ADD CONSTRAINT query_challenges_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: sql_practice_history sql_practice_history_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_practice_history
    ADD CONSTRAINT sql_practice_history_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: sql_practice_history sql_practice_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_practice_history
    ADD CONSTRAINT sql_practice_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict yM3qzlejMg4gN7qa8a1azEaf5x8J4UPt4X0DHIWQqpUWXybOFlIFBRdOonTCwMO

