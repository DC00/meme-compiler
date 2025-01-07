--liquibase formatted sql

--changeset daniel.coo:1
--comment: add videos table
create table videos (
    id bigint primary key,
    uuid uuid not null,
    url varchar(255) not null
)
--rollback DROP TABLE videos;
