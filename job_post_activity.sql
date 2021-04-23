-- public.job_post_activity definition

-- Drop table

-- DROP TABLE public.job_post_activity;

CREATE TABLE public.job_post_activity (
	id serial NOT NULL,
	user_id int4 NOT NULL,
	job_post_id int4 NOT NULL,
	apply_date timestamp NOT NULL,
	CONSTRAINT job_post_activity_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_job_post_activity_id ON public.job_post_activity USING btree (id);


-- public.job_post_activity foreign keys

ALTER TABLE public.job_post_activity ADD CONSTRAINT job_post_activity_job_post_id_fkey FOREIGN KEY (job_post_id) REFERENCES public.job_post(id);
ALTER TABLE public.job_post_activity ADD CONSTRAINT job_post_activity_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);

INSERT INTO public.job_post_activity (id,user_id,job_post_id,apply_date) VALUES
	 (15,1,2,'2021-04-21 14:00:09.054726'),
	 (16,1,1,'2021-04-21 14:00:24.846156'),
	 (17,2,1,'2021-04-22 07:46:01.488526'),
	 (18,3,5,'2021-04-22 23:03:11.592238'),
	 (19,4,4,'2021-04-22 23:03:40.655664'),
	 (20,3,1,'2021-04-22 23:03:48.018537'),
	 (21,2,2,'2021-04-22 23:21:38.237491'),
	 (22,3,3,'2021-04-22 23:21:45.026161'),
	 (23,5,5,'2021-04-22 23:21:56.992672'),
	 (24,6,6,'2021-04-22 23:22:04.128722');
INSERT INTO public.job_post_activity (id,user_id,job_post_id,apply_date) VALUES
	 (25,8,7,'2021-04-22 23:22:15.042126'),
	 (26,8,8,'2021-04-22 23:22:27.583179'),
	 (28,9,6,'2021-04-22 23:22:43.792486');