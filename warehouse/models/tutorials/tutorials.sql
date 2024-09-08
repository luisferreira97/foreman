with source_data as (
    select 1 as id
    union all
    select '' as speaker_id
    union all
    select '' as title
    union all
    select '' as summary
    union all
    select ''::date as date
    union all
    select '' as schedule
    union all
    select 60 as duration
)
select * from source_data